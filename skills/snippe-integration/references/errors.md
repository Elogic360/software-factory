# Error Handling

Every Snippe response uses the same envelope, so your error handling can be uniform across all endpoints. This file documents the shape, the status codes and error codes you'll see, the common failure patterns, and how to recover from each.

Read the [`PAY_001` section](#the-pay_001-gotcha) first if you're debugging a cryptic "failed to initiate payment" error — it's almost always caused by something very specific and easy to fix.

## Table of contents

- [Response envelope](#response-envelope)
- [HTTP status codes](#http-status-codes)
- [Error codes](#error-codes)
- [The PAY_001 gotcha](#the-pay_001-gotcha)
- [Common error examples](#common-error-examples)
- [Validation rules](#validation-rules)
- [Recovery patterns](#recovery-patterns)

## Response envelope

Success:

```json
{
  "status": "success",
  "code": 200,
  "data": { /* ... */ }
}
```

Error:

```json
{
  "status": "error",
  "code": 400,
  "error_code": "validation_error",
  "message": "amount is required"
}
```

The HTTP status matches `code`. Dispatch on `error_code` (stable string) rather than `message` (human-readable, subject to copy changes).

## HTTP status codes

| Code | Meaning                                          |
| ---- | ------------------------------------------------ |
| 200  | OK                                               |
| 201  | Created                                          |
| 400  | Bad request — validation error or malformed JSON |
| 401  | Unauthorized — missing or invalid API key        |
| 403  | Forbidden — authenticated but lacks scope        |
| 404  | Not found                                        |
| 409  | Conflict                                         |
| 422  | Unprocessable entity — idempotency key mismatch  |
| 429  | Too many requests — rate limited                 |
| 500  | Internal server error                            |
| 503  | Service unavailable                              |

## Error codes

These are the `error_code` values you should expect:

| Code                  | Meaning                                                    |
| --------------------- | ---------------------------------------------------------- |
| `unauthorized`        | Invalid or missing API key                                 |
| `insufficient_scope`  | API key is valid but lacks the required scope              |
| `validation_error`    | One or more fields in the request are invalid              |
| `not_found`           | Resource doesn't exist                                     |
| `conflict`            | Resource state conflict                                    |
| `payment_failed`      | Payment processing error (e.g. insufficient balance)       |
| `rate_limit_exceeded` | Too many requests in the current rate-limit window         |
| `PAY_001`             | Failed to initiate payment — see below                     |

## The PAY_001 gotcha

`PAY_001` is the error code you'll see most often when something unexpected goes wrong on `POST /v1/payments` or `POST /v1/payouts/send`. The message is typically just "failed to initiate payment," which isn't very actionable. The error has **two possible causes**, and you should check them in this order:

1. **Your `Idempotency-Key` header is longer than 30 characters.** This is the single most common cause, and it's silent — the API doesn't clearly label it. Any key > 30 chars returns `PAY_001` even though the underlying issue is a header validation error. Check your code for things like `` `${userId}-${orderId}-${Date.now()}` `` which easily overshoots 30 characters.
2. **The upstream payment processor (Selcom) is temporarily unavailable.** If your idempotency key is fine, retry with exponential backoff.

**When debugging `PAY_001`**: count the length of your idempotency key *first*. Print it, measure it, check it in a REPL. If it's ≤ 30 characters and you still get `PAY_001`, then it's a processor issue — retry with backoff.

Safe idempotency key patterns (all under 30 characters):

- `ord-ABC12345-t1` (15 chars)
- `pay-8f3a9b2c-1` (14 chars)
- `<6-char-prefix>-<16-char-uuid-fragment>` (23 chars)

Unsafe patterns to avoid:

- `` `order-${orderId}-user-${userId}-${Date.now()}` `` — easily 50+ chars
- Full UUIDs with a prefix — UUIDs are 36 chars alone, blowing the limit before you add anything
- Base64-encoded JSON — verbose and unpredictable in length

## Common error examples

### Invalid API key (401)

```json
{
  "status": "error",
  "code": 401,
  "error_code": "unauthorized",
  "message": "invalid or missing API key"
}
```

Check the `Authorization: Bearer snp_...` header. Common mistakes: typo in the key, the key was rotated, or the env var is unset in the current environment.

### Insufficient scope (403)

```json
{
  "status": "error",
  "code": 403,
  "error_code": "insufficient_scope",
  "message": "API key lacks disbursement:create scope"
}
```

Create a new API key in the dashboard with the required scopes, or add the missing scope to the existing key.

### Missing required field (400)

```json
{
  "status": "error",
  "code": 400,
  "error_code": "validation_error",
  "message": "amount is required"
}
```

Check the required fields lists in `references/payments.md` or `references/disbursements.md` for the specific endpoint you're calling. Card payments require the most fields (full customer address block); QR payments require the fewest.

### Invalid phone number (400)

```json
{
  "status": "error",
  "code": 400,
  "error_code": "validation_error",
  "message": "phone_number must be a valid phone number"
}
```

Use `255XXXXXXXXX` or `+255XXXXXXXXX` for Tanzanian numbers. Local formats like `0781000000` are rejected. If you're accepting user input, normalise it: strip any leading `0`, then prepend `255`.

### Amount below minimum (400)

```json
{
  "status": "error",
  "code": 400,
  "error_code": "validation_error",
  "message": "amount 100 is below minimum of 500"
}
```

Minimum is 500 TZS for payments, 5000 TZS for payouts. Snippe amounts are integers in the smallest currency unit — `100` means 100 TZS, not 1.00.

### Insufficient balance for payout (500)

```json
{
  "status": "error",
  "code": 500,
  "error_code": "payment_failed",
  "message": "insufficient balance: available 5000, required 6500"
}
```

The total deducted is `amount + fees`. Call `GET /v1/payouts/fee?amount=X` to calculate the fee first, then check `GET /v1/payments/balance` before attempting the payout — see `references/disbursements.md` for the full preflight pattern.

### Idempotency conflict (422)

```json
{
  "status": "error",
  "code": 422,
  "error_code": "validation_error",
  "message": "idempotency key already used with different request body"
}
```

You reused an idempotency key but changed the request body. Use a different key — idempotency keys must be unique per unique request body. This usually indicates a bug where the client is deriving the key from something less unique than the request contents (e.g. using only the user ID instead of user ID + order ID + amount).

### Rate limit exceeded (429)

```json
{
  "status": "error",
  "code": 429,
  "error_code": "rate_limit_exceeded",
  "message": "Too many requests"
}
```

Respect the `X-Ratelimit-Reset` header (seconds until the window resets) before retrying. Implement exponential backoff with jitter to avoid stampede.

## Validation rules

The rules that are checked server-side on every request:

| Rule              | Constraint                                  |
| ----------------- | ------------------------------------------- |
| Min payment       | 500 TZS                                     |
| Min payout        | 5,000 TZS                                   |
| Currency          | `TZS` only                                  |
| Amount format     | Integer in smallest currency unit           |
| Phone number      | `255XXXXXXXXX` or `+255XXXXXXXXX`           |
| Webhook/redirect  | HTTPS, max 500 characters                   |
| Idempotency key   | Max 30 characters                           |

Validate client-side in the same order to give better error messages and reduce round-trips.

## Recovery patterns

Different errors need different recovery strategies. A well-behaved client handles each of these distinctly:

- **5xx errors and network failures** — Retry with exponential backoff and jitter. Start at ~1s, double each time, cap at ~60s, give up after 5–6 attempts. Use the same `Idempotency-Key` across retries so the server can dedupe.
- **429 rate limit** — Read `X-Ratelimit-Reset` and wait that many seconds before the next attempt. Don't retry faster than the reset tells you to — you'll just get 429 again.
- **422 idempotency conflict** — Stop retrying this request. The server already processed a different request with the same key. Generate a new key derived from the new body (e.g. hash the body's semantically-meaningful fields and truncate to ≤ 30 chars).
- **400 validation_error** — Do not retry. Fix the request and try again. These are permanent for this request shape.
- **401 unauthorized** — Do not retry. The key is wrong or unset; surface this to the developer.
- **403 insufficient_scope** — Do not retry. Create or upgrade an API key with the missing scope.
- **`PAY_001`** — First check idempotency key length (≤ 30 chars). If the key is fine, retry with backoff as for 5xx.
- **`insufficient balance`** — Do not retry blindly. Either top up the balance or reconcile with `GET /v1/payments/balance` to understand the actual shortfall.

### Retry example (pseudocode)

```
attempt = 0
max_attempts = 6
while attempt < max_attempts:
  try:
    return snippe_call(body, idempotency_key)
  except HttpError as e:
    if e.status == 429:
      sleep(int(e.headers["X-Ratelimit-Reset"]))
    elif e.status >= 500 or e.error_code == "PAY_001":
      sleep(min(60, 2 ** attempt) + random.uniform(0, 1))
    elif e.status == 422 or e.status == 400:
      raise  # Don't retry validation failures
    else:
      raise
    attempt += 1
raise Error("Max retries exceeded")
```

Always pass the same idempotency key across the retry loop — that's the whole point of idempotency keys, and it's safe because the server will return the cached response if the first attempt actually succeeded but the network swallowed the response.
