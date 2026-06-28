# Webhooks

Webhooks deliver real-time notifications when something happens on your account — a payment completes, a payout fails, etc. Snippe sends an HTTP `POST` to your configured `webhook_url` with a signed JSON payload. Your job is to verify the signature, deduplicate, respond quickly, and process asynchronously.

This file covers everything you need to build a correct webhook handler. The signature verification section is the most important — getting it wrong means your endpoint will reject legitimate events (or, worse, accept spoofed ones).

## Table of contents

- [Event types](#event-types)
- [Request headers](#request-headers)
- [Payload envelope](#payload-envelope)
- [The data.amount gotcha](#the-dataamount-gotcha)
- [Signature verification](#signature-verification)
- [Node.js example (Express)](#nodejs-example-express)
- [Python example (Flask)](#python-example-flask)
- [PHP example](#php-example)
- [Go example](#go-example)
- [Retry logic](#retry-logic)
- [Best practices checklist](#best-practices-checklist)

## Event types

| Event               | Fires when…                              |
| ------------------- | ---------------------------------------- |
| `payment.completed` | A payment is successfully processed      |
| `payment.failed`    | A payment fails (decline, timeout, etc.) |
| `payment.voided`    | A payment is cancelled before completion |
| `payment.expired`   | A payment expires (4-hour timeout)       |
| `payout.completed`  | A payout is successfully delivered       |
| `payout.failed`     | A payout fails                           |
| `payout.reversed`   | A payout is reversed after completion    |

## Request headers

Every webhook POST includes:

| Header                | Value                                 |
| --------------------- | ------------------------------------- |
| `Content-Type`        | `application/json`                    |
| `User-Agent`          | `Snippe-Webhook/1.0`                  |
| `X-Webhook-Event`     | Event type (e.g. `payment.completed`) |
| `X-Webhook-Timestamp` | Unix timestamp (seconds) of the event |
| `X-Webhook-Signature` | Hex-encoded HMAC-SHA256 signature     |

Use `X-Webhook-Event` only as a hint — the authoritative event type is `type` inside the verified payload. Don't route on the header before checking the signature.

## Payload envelope

All v2026-01-25 webhooks share this envelope. The outer fields (`id`, `type`, `api_version`, `created_at`) are stable across every event; `data` varies by event type.

```json
{
  "id": "evt_a1b2c3d4e5f6g7h8i9j0",
  "type": "payment.completed",
  "api_version": "2026-01-25",
  "created_at": "2026-01-24T10:30:00Z",
  "data": {
    "reference": "pi_a1b2c3d4e5f6",
    "external_reference": "SEL123456789",
    "status": "completed",
    "amount": { "value": 50000, "currency": "TZS" },
    "settlement": {
      "gross": { "value": 50000, "currency": "TZS" },
      "fees":  { "value": 1000,  "currency": "TZS" },
      "net":   { "value": 49000, "currency": "TZS" }
    },
    "channel": { "type": "mobile_money", "provider": "mpesa" },
    "customer": {
      "phone": "+255712345678",
      "name": "John Doe",
      "email": "john@example.com"
    },
    "metadata": { "order_id": "ORD-12345" },
    "completed_at": "2026-01-24T10:30:00Z"
  }
}
```

- `id` — use this as your deduplication key. Snippe may deliver the same event more than once; your handler must be idempotent.
- `type` — dispatch on this, not the header.
- `data.reference` — the Snippe-side reference for the payment/payout, matches the `reference` you got back from `POST /v1/payments` or `POST /v1/payouts/send`.
- `data.external_reference` — the upstream processor's reference (useful for customer support and reconciliation).
- `data.settlement` — for payments: the breakdown of gross amount, fees charged by Snippe, and net credited to your balance.
- `data.metadata` — whatever you passed in on create, echoed back.

## The data.amount gotcha

**In webhook payloads, `data.amount` is an object `{value, currency}`, not a plain integer like in request bodies.** This bites integrations that assume symmetry between request and webhook shapes.

```json
// Request body (integer):
"details": { "amount": 50000, "currency": "TZS" }

// Webhook data (object):
"data": { "amount": { "value": 50000, "currency": "TZS" } }
```

When parsing webhook payloads, read `data.amount.value` and `data.amount.currency` separately. If your code does `data.amount === 50000` it will always be false. The same pattern applies to `settlement.gross`, `settlement.fees`, and `settlement.net` — all are objects in webhooks.

## Signature verification

Snippe signs every webhook with HMAC-SHA256. **Verify every webhook in production** — without verification, anyone who knows your URL can forge events and corrupt your ledger.

**Get your signing key** from the Snippe Dashboard under **Settings → Webhook Secret**. It's a separate secret from your API key — don't confuse them. You can also fetch it via:

```http
GET /api/v1/settings/webhook-secret
Authorization: Bearer <jwt_token>
```

**How signatures are computed:**

```
X-Webhook-Signature = hex(HMAC-SHA256(signing_key, "{timestamp}.{raw_body}"))
```

The signed message is the literal string `{timestamp}.{raw_body}` — a dot joining the timestamp header and the raw request body as received.

**Verification steps**:

1. Extract `X-Webhook-Timestamp` and `X-Webhook-Signature` from the headers.
2. **Read the raw request body as bytes/string — do NOT parse and re-serialize the JSON.** Re-serialization changes whitespace, key ordering, number formatting, etc., and any of these will break the signature.
3. Construct the message: `{timestamp}.{raw_body}`.
4. Compute HMAC-SHA256 with your signing key and hex-encode the result.
5. Compare with `X-Webhook-Signature` using **constant-time comparison** to prevent timing attacks.
6. **Reject requests where the timestamp is more than 5 minutes old** to prevent replay attacks. A captured old webhook would otherwise still have a valid signature.
7. Only after all checks pass, parse the JSON and act on it.

### Reading the raw body in each framework

- **Express.js**: `express.raw({ type: "application/json" })` — gives you `req.body` as a Buffer.
- **Flask**: `request.get_data(as_text=True)` — returns the raw string before Flask parses.
- **Django**: `request.body` — the raw bytes, always available.
- **FastAPI**: `await request.body()` — returns raw bytes.
- **Go stdlib**: `io.ReadAll(req.Body)` before any `json.NewDecoder`. Re-insert the bytes with `req.Body = io.NopCloser(bytes.NewReader(b))` if a downstream handler also needs them.
- **PHP**: `file_get_contents("php://input")`.
- **Rails**: `request.raw_post`.

## Node.js example (Express)

```javascript
const crypto = require("crypto");
const express = require("express");
const app = express();

function verifyWebhook(rawBody, headers, signingKey) {
  const timestamp = headers["x-webhook-timestamp"];
  const signature = headers["x-webhook-signature"];

  if (!timestamp || !signature) {
    throw new Error("Missing webhook headers");
  }

  // Prevent replay attacks
  const eventTime = parseInt(timestamp, 10);
  const currentTime = Math.floor(Date.now() / 1000);
  if (currentTime - eventTime > 300) {
    throw new Error("Webhook timestamp too old");
  }

  // Compute expected signature over raw body
  const message = `${timestamp}.${rawBody}`;
  const expected = crypto
    .createHmac("sha256", signingKey)
    .update(message)
    .digest("hex");

  // Constant-time compare
  const sigBuf = Buffer.from(signature);
  const expBuf = Buffer.from(expected);
  if (sigBuf.length !== expBuf.length ||
      !crypto.timingSafeEqual(sigBuf, expBuf)) {
    throw new Error("Invalid webhook signature");
  }

  return JSON.parse(rawBody);
}

// Use express.raw — DO NOT use express.json on the webhook route
app.post(
  "/webhooks/snippe",
  express.raw({ type: "application/json" }),
  (req, res) => {
    try {
      const event = verifyWebhook(
        req.body.toString("utf8"),
        req.headers,
        process.env.SNIPPE_WEBHOOK_SECRET,
      );

      // Deduplicate by event.id before processing
      switch (event.type) {
        case "payment.completed":
          handlePaymentCompleted(event.data);
          break;
        case "payment.failed":
          handlePaymentFailed(event.data);
          break;
        // ... other event types
      }

      res.status(200).send("OK");
    } catch (err) {
      console.error("Webhook verification failed:", err.message);
      res.status(400).send("Invalid signature");
    }
  },
);
```

Mount `express.raw` **only on this route**, not globally — other routes probably still want `express.json()`.

## Python example (Flask)

```python
import hmac
import hashlib
import time
import json
from flask import Flask, request, abort

app = Flask(__name__)

def verify_webhook(raw_body: str, headers, signing_key: str) -> dict:
    timestamp = headers.get("X-Webhook-Timestamp")
    signature = headers.get("X-Webhook-Signature")

    if not timestamp or not signature:
        raise ValueError("Missing webhook headers")

    # Replay protection
    if time.time() - int(timestamp) > 300:
        raise ValueError("Webhook timestamp too old")

    message = f"{timestamp}.{raw_body}".encode("utf-8")
    expected = hmac.new(
        signing_key.encode("utf-8"),
        message,
        hashlib.sha256,
    ).hexdigest()

    # hmac.compare_digest is constant-time
    if not hmac.compare_digest(signature, expected):
        raise ValueError("Invalid webhook signature")

    return json.loads(raw_body)

@app.post("/webhooks/snippe")
def snippe_webhook():
    try:
        # get_data(as_text=True) returns the raw body before Flask parses
        event = verify_webhook(
            request.get_data(as_text=True),
            request.headers,
            os.environ["SNIPPE_WEBHOOK_SECRET"],
        )
    except ValueError as e:
        abort(400, str(e))

    # Deduplicate by event["id"] before processing
    if event["type"] == "payment.completed":
        handle_payment_completed(event["data"])

    return ("OK", 200)
```

## PHP example

```php
<?php
function verify_webhook(string $raw_body, array $headers, string $signing_key): array {
    $timestamp = $headers['X-Webhook-Timestamp'] ?? null;
    $signature = $headers['X-Webhook-Signature'] ?? null;

    if (!$timestamp || !$signature) {
        throw new Exception('Missing webhook headers');
    }

    // Replay protection
    if (time() - (int)$timestamp > 300) {
        throw new Exception('Webhook timestamp too old');
    }

    $message = $timestamp . '.' . $raw_body;
    $expected = hash_hmac('sha256', $message, $signing_key);

    // hash_equals is constant-time
    if (!hash_equals($expected, $signature)) {
        throw new Exception('Invalid webhook signature');
    }

    return json_decode($raw_body, true);
}

// Handler
$raw = file_get_contents('php://input');
try {
    $event = verify_webhook($raw, getallheaders(), getenv('SNIPPE_WEBHOOK_SECRET'));
} catch (Exception $e) {
    http_response_code(400);
    exit('Invalid signature');
}
// Deduplicate by $event['id'] and dispatch on $event['type']
http_response_code(200);
echo 'OK';
```

## Go example

```go
package webhook

import (
    "bytes"
    "crypto/hmac"
    "crypto/sha256"
    "encoding/hex"
    "encoding/json"
    "errors"
    "io"
    "net/http"
    "os"
    "strconv"
    "time"
)

type Event struct {
    ID         string          `json:"id"`
    Type       string          `json:"type"`
    APIVersion string          `json:"api_version"`
    CreatedAt  string          `json:"created_at"`
    Data       json.RawMessage `json:"data"`
}

func verifyWebhook(rawBody []byte, headers http.Header, signingKey string) (*Event, error) {
    timestamp := headers.Get("X-Webhook-Timestamp")
    signature := headers.Get("X-Webhook-Signature")
    if timestamp == "" || signature == "" {
        return nil, errors.New("missing webhook headers")
    }

    // Replay protection
    ts, err := strconv.ParseInt(timestamp, 10, 64)
    if err != nil {
        return nil, errors.New("bad timestamp")
    }
    if time.Now().Unix()-ts > 300 {
        return nil, errors.New("webhook timestamp too old")
    }

    mac := hmac.New(sha256.New, []byte(signingKey))
    mac.Write([]byte(timestamp + "."))
    mac.Write(rawBody)
    expected := hex.EncodeToString(mac.Sum(nil))

    // hmac.Equal is constant-time
    if !hmac.Equal([]byte(expected), []byte(signature)) {
        return nil, errors.New("invalid webhook signature")
    }

    var event Event
    if err := json.Unmarshal(rawBody, &event); err != nil {
        return nil, err
    }
    return &event, nil
}

func Handler(w http.ResponseWriter, r *http.Request) {
    // Read the body first — don't decode yet
    raw, err := io.ReadAll(r.Body)
    if err != nil {
        http.Error(w, "read error", http.StatusBadRequest)
        return
    }
    // Allow any downstream middleware to re-read the body
    r.Body = io.NopCloser(bytes.NewReader(raw))

    event, err := verifyWebhook(raw, r.Header, os.Getenv("SNIPPE_WEBHOOK_SECRET"))
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    // Deduplicate by event.ID, dispatch on event.Type
    _ = event
    w.WriteHeader(http.StatusOK)
    w.Write([]byte("OK"))
}
```

## Retry logic

If your endpoint returns non-2xx, times out, or is unreachable, Snippe retries with exponential backoff:

| Attempt | Delay after previous failure |
| ------- | ---------------------------- |
| 1       | Immediate                    |
| 2       | 3 minutes                    |
| 3       | 6 minutes                    |
| 4       | 12 minutes                   |
| 5       | 24 minutes                   |

After 5 failed attempts the webhook is marked `abandoned` and will not be retried automatically — you'd have to reconcile via `GET /v1/payments/{reference}` or `GET /v1/payouts/{reference}` instead.

The practical implication: **respond 2xx within 30 seconds** and do the real work asynchronously. Don't block the webhook response on a database write, a downstream API call, or an email send. Push the event onto a queue (SQS, Redis, PostgreSQL job table, etc.) and return 200 immediately.

## Best practices checklist

Every webhook handler should satisfy all of these:

- [ ] **Verify the signature** on every request in production.
- [ ] **Read the raw body** — don't use middleware that parses JSON before you compute the HMAC.
- [ ] **Use constant-time comparison** (`crypto.timingSafeEqual`, `hmac.compare_digest`, `hash_equals`, `hmac.Equal`).
- [ ] **Validate timestamp freshness** — reject if older than 5 minutes.
- [ ] **Deduplicate by `event.id`** — store seen IDs for at least a few hours; returning early on a duplicate is safe.
- [ ] **Respond 2xx within 30 seconds** — enqueue the work and process async.
- [ ] **Serve over HTTPS** — the webhook URL must be HTTPS; plain HTTP is rejected on create.
- [ ] **Log failures** — keep the raw body, headers, and signature computation output around so you can debug signature mismatches when they happen.
- [ ] **Treat `X-Webhook-Event` as a hint** — always trust the verified `event.type` from the body.
