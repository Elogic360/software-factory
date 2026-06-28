# Payments

The Payments API collects money from customers via three channels: **mobile money**, **card**, and **dynamic QR**. Use this API when you want full control over the UI. If you want a pre-built hosted checkout page instead, use Sessions (`references/sessions.md`).

## Table of contents

- [Endpoints](#endpoints)
- [Payment status lifecycle](#payment-status-lifecycle)
- [Currency and amount rules](#currency-and-amount-rules)
- [Mobile money payments](#mobile-money-payments)
- [Card payments](#card-payments)
- [Dynamic QR payments](#dynamic-qr-payments)
- [Account balance](#account-balance)

## Endpoints

| Endpoint                        | Method | Description           |
| ------------------------------- | ------ | --------------------- |
| `/v1/payments`                  | POST   | Create payment intent |
| `/v1/payments`                  | GET    | List all payments     |
| `/v1/payments/{reference}`      | GET    | Get payment status    |
| `/v1/payments/{reference}/push` | POST   | Re-trigger USSD push  |
| `/v1/payments/balance`          | GET    | Get account balance   |
| `/v1/payments/search`           | GET    | Search payments       |

All creates (`POST /v1/payments`) should include an `Idempotency-Key` header (≤30 characters) to make retries safe.

## Payment status lifecycle

| Status      | Meaning                                   |
| ----------- | ----------------------------------------- |
| `pending`   | Created, awaiting customer action         |
| `completed` | Successful, funds received                |
| `failed`    | Declined, timed out, or otherwise failed  |
| `voided`    | Cancelled before completion               |
| `expired`   | Not authorised within 4 hours             |

The response from `POST /v1/payments` is always `pending` initially. The terminal state arrives via webhook (`references/webhooks.md`) or via polling `GET /v1/payments/{reference}`.

## Currency and amount rules

- Only **TZS** is supported — sending any other currency returns `400 validation_error`.
- Amounts are **integers** in the smallest currency unit. `500` means 500 TZS. No decimals.
- **Minimum payment amount is 500 TZS.** Values below this return `"amount 100 is below minimum of 500"`.

## Mobile money payments

The customer receives a USSD push on their phone. Supported networks: **Airtel Money, M-Pesa, Mixx by Yas, Halotel**. Snippe auto-detects the network from the phone number.

### Request

```http
POST /v1/payments
Authorization: Bearer snp_your_api_key_here
Content-Type: application/json
Idempotency-Key: order-12345-attempt-1
```

```json
{
  "payment_type": "mobile",
  "details": {
    "amount": 500,
    "currency": "TZS"
  },
  "phone_number": "255781000000",
  "customer": {
    "firstname": "FirstName",
    "lastname": "LastName",
    "email": "customer@email.com"
  },
  "webhook_url": "https://yoursite.com/webhooks/snippe",
  "metadata": {
    "order_id": "ORD-12345"
  }
}
```

### Required fields

- `payment_type` — must be the string `"mobile"`
- `details.amount` — integer, ≥ 500
- `details.currency` — must be `"TZS"`
- `phone_number` — format `255XXXXXXXXX` (or `+255XXXXXXXXX`)
- `customer.firstname`, `customer.lastname`, `customer.email`

### Response

```json
{
  "status": "success",
  "code": 201,
  "data": {
    "amount": { "currency": "TZS", "value": 500 },
    "api_version": "2026-01-25",
    "expires_at": "2026-01-25T05:04:54.063993853Z",
    "object": "payment",
    "payment_type": "mobile",
    "reference": "9015c155-9e29-4e8e-8fe6-d5d81553c8e6",
    "status": "pending"
  }
}
```

### Flow

1. You call `POST /v1/payments` and receive a `reference` with `status: "pending"`.
2. Snippe triggers a USSD push to the customer's phone.
3. The customer enters their mobile money PIN to authorise.
4. Snippe sends a webhook (`payment.completed` or `payment.failed`) to your `webhook_url`.
5. If the push wasn't delivered, you can re-trigger it with `POST /v1/payments/{reference}/push`.
6. If not authorised within 4 hours, the payment transitions to `expired`.

### Notes

- `metadata` is an arbitrary key-value bag you can use to correlate payments with your internal order IDs. It's echoed back in webhooks and GET responses.
- Store the `reference` from the response — that's your handle for looking up the payment later.

## Card payments

Customers are redirected to a secure hosted checkout page (Selcom). Supported: Visa, Mastercard, and local debit cards.

### Request

```json
{
  "payment_type": "card",
  "details": {
    "amount": 1000,
    "currency": "TZS",
    "redirect_url": "https://your_domain.com/payment_done",
    "cancel_url": "https://your_domain.com/payment_failed"
  },
  "phone_number": "255781000000",
  "customer": {
    "firstname": "FirstName",
    "lastname": "LastName",
    "email": "customer@email.com",
    "address": "Customer Address",
    "city": "Customer City",
    "state": "DSM",
    "postcode": "14101",
    "country": "TZ"
  },
  "webhook_url": "https://yoursite.com/webhooks/snippe",
  "metadata": { "order_id": "ORD-12345" }
}
```

### Required fields

Card payments require the full customer address block — more than mobile money or QR:

- `payment_type` — `"card"`
- `details.amount`, `details.currency`
- `details.redirect_url` — where to send the customer after a successful card charge
- `details.cancel_url` — where to send them if they abandon or the card is declined
- `phone_number`
- `customer.firstname`, `customer.lastname`, `customer.email`
- `customer.address`, `customer.city`, `customer.state`, `customer.postcode`
- `customer.country` — ISO 3166-1 alpha-2 code (e.g. `"TZ"`)

### Response

```json
{
  "status": "success",
  "code": 201,
  "data": {
    "amount": { "currency": "TZS", "value": 1000 },
    "expires_at": "2026-01-25T01:32:10.476693917Z",
    "payment_url": "https://tz.selcom.online/paymentgw/checkout/...",
    "payment_token": "63891931",
    "payment_type": "card",
    "reference": "2e0bcc5f-92ca-44f9-8c1b-4d2966d9921f",
    "status": "pending"
  }
}
```

The important new field is `payment_url` — redirect the customer to this URL so they can enter their card details on Selcom's secure checkout. Do not try to collect card details in your own UI.

### Flow

1. Create the payment.
2. Redirect the customer's browser to `payment_url`.
3. The customer enters card details and authorises on Selcom.
4. Selcom redirects the customer back to your `redirect_url` (success) or `cancel_url` (failure/abandon).
5. Snippe sends a webhook with the definitive result — trust the webhook, not the redirect URL, for settlement state.

## Dynamic QR payments

Generate a QR code the customer scans with their mobile money app. Typical use case: in-person POS or printed invoices.

### Request

```json
{
  "payment_type": "dynamic-qr",
  "details": {
    "amount": 500,
    "currency": "TZS",
    "redirect_url": "https://your_domain.com/payment_done",
    "cancel_url": "https://your_domain.com/payment_failed"
  },
  "phone_number": "255781000000",
  "customer": {
    "firstname": "FirstName",
    "lastname": "LastName",
    "email": "customer@email.com"
  },
  "webhook_url": "https://yoursite.com/webhooks/snippe",
  "metadata": { "order_id": "ORD-12345" }
}
```

### Required fields

Only the core three are strictly required — unlike card payments, customer fields are optional for QR:

- `payment_type` — `"dynamic-qr"`
- `details.amount`, `details.currency`

Customer fields, `phone_number`, and webhook URL are optional but recommended for reconciliation.

### Response

```json
{
  "status": "success",
  "code": 201,
  "data": {
    "amount": { "currency": "TZS", "value": 500 },
    "expires_at": "2026-01-25T04:47:50.159178853Z",
    "payment_qr_code": "000201010212041552545429990002026390014tz.go.bot.tips...",
    "payment_token": "63890400",
    "payment_url": "https://tz.selcom.online/paymentgw/checkout/...",
    "payment_type": "dynamic-qr",
    "reference": "6a490816-799b-4fc9-b9b6-2ec67c54e17e",
    "status": "pending"
  }
}
```

The key field is `payment_qr_code` — a string encoding the EMV QR payload. Render it as a QR code image on whatever surface your customer scans (POS screen, printed receipt, in-app display). Any QR library that accepts raw data (e.g. `qrcode` in Python, `qrcode` in Node, `zxing` in Java) will work.

### Flow

1. Create the payment and receive the `payment_qr_code` string.
2. Render it as a QR image on your POS / screen / receipt.
3. Customer opens their mobile money app, scans the QR, confirms the amount.
4. Snippe sends a webhook with the result.

## Account balance

Check your available funds. Useful before payouts, or as a diagnostic when `insufficient balance` errors show up.

```http
GET /v1/payments/balance
Authorization: Bearer snp_your_api_key_here
```

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "available": { "currency": "TZS", "value": 6943 },
    "balance":   { "currency": "TZS", "value": 6943 },
    "object": "balance"
  }
}
```

`available` is what you can immediately spend on payouts. `balance` may include funds still settling. For payout preflight checks, use `available`.
