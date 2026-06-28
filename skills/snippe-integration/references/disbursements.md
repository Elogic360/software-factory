# Disbursements (Payouts)

The Disbursements API sends money **out** to recipients — mobile money wallets or bank accounts. Typical use cases: payroll, vendor payments, refunds, marketplace seller payouts, loan disbursements.

**Balance accounting**: The total amount (payout + fees) is deducted from your available balance **immediately** when the payout is created. If the payout later fails, funds are automatically returned to your balance. Always calculate fees before creating payouts so you don't trip the `insufficient balance` error.

## Table of contents

- [Endpoints](#endpoints)
- [Payout status lifecycle](#payout-status-lifecycle)
- [Calculate fee before payout](#calculate-fee-before-payout)
- [Mobile money payout](#mobile-money-payout)
- [Bank transfer payout](#bank-transfer-payout)
- [Supported bank codes](#supported-bank-codes)

## Endpoints

| Endpoint                  | Method | Description          |
| ------------------------- | ------ | -------------------- |
| `/v1/payouts/send`        | POST   | Create payout        |
| `/v1/payouts`             | GET    | List payouts         |
| `/v1/payouts/{reference}` | GET    | Get payout status    |
| `/v1/payouts/fee`         | GET    | Calculate payout fee |

Use an `Idempotency-Key` header (≤30 characters) on `POST /v1/payouts/send`. Payroll runs are a textbook case for idempotency — if your retry logic fires twice you want the second call to return the cached response, not double-pay the employee.

## Payout status lifecycle

| Status      | Meaning                                     |
| ----------- | ------------------------------------------- |
| `pending`   | Created, awaiting processing                |
| `completed` | Recipient received funds                    |
| `failed`    | Failed — see `failure_reason` in the payload |
| `reversed`  | Reversed after completion                   |

As with payments, the initial response is always `pending`. The terminal state arrives via webhook (`references/webhooks.md`). Minimum payout amount is **5,000 TZS** — smaller amounts return a validation error.

## Calculate fee before payout

Always call `GET /v1/payouts/fee` before creating a payout. This is the cleanest way to preflight: you learn both the fee and the total that will be deducted, and you can compare against your balance before committing.

```http
GET /v1/payouts/fee?amount=50000
Authorization: Bearer snp_your_api_key_here
```

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "amount": 50000,
    "fee_amount": 1000,
    "total_amount": 51000,
    "currency": "TZS"
  }
}
```

**Pattern for safe payout creation**:

1. Call `GET /v1/payouts/fee?amount=X` → note `total_amount`.
2. Call `GET /v1/payments/balance` → check `available.value ≥ total_amount`.
3. Only if you have the balance, call `POST /v1/payouts/send`.

This prevents the race where two concurrent payouts each think they have enough balance but together exceed it. For high-concurrency payroll, serialise the balance check + payout create into a single critical section in your application.

## Mobile money payout

Send TZS to Airtel Money, M-Pesa, Mixx by Yas, or HaloPesa. Snippe auto-detects the provider from the phone number — you don't specify it.

### Request

```http
POST /v1/payouts/send
Authorization: Bearer <api_key>
Content-Type: application/json
Idempotency-Key: payout-emp-001-jan-2026
```

```json
{
  "amount": 5000,
  "channel": "mobile",
  "recipient_phone": "255781000000",
  "recipient_name": "Recipient Name",
  "narration": "Salary payment January 2026",
  "webhook_url": "https://yoursite.com/webhooks/snippe",
  "metadata": {
    "employee_id": "EMP-001",
    "payroll_id": "PAY-2026-01"
  }
}
```

### Required fields

- `amount` — integer ≥ 5000 TZS
- `channel` — `"mobile"`
- `recipient_phone` — format `255XXXXXXXXX` (or `+255XXXXXXXXX`)
- `recipient_name` — the recipient's name (appears in Snippe's records and sometimes on the recipient's SMS)

Optional but useful:
- `narration` — free-text note attached to the payout (shows in the recipient's mobile money statement)
- `webhook_url` — per-payout override
- `metadata` — for linking to internal payroll records, invoice IDs, etc.

### Response

```json
{
  "status": "success",
  "code": 201,
  "data": {
    "amount":   { "currency": "TZS", "value": 5000 },
    "channel":  { "provider": "airtel", "type": "mobile_money" },
    "external_reference": "fVJQRPGYbtN3",
    "fees":     { "currency": "TZS", "value": 1500 },
    "recipient": { "name": "Recipient Name", "phone": "255781000000" },
    "reference": "667c9279-846f-4001-b046-fdecab204f4f",
    "status": "pending",
    "total":    { "currency": "TZS", "value": 6500 }
  }
}
```

Note `channel.provider` — the auto-detected network (`"airtel"`, `"mpesa"`, `"mixx"`, or `"halotel"`). `total` is what was debited from your balance (`amount + fees`).

## Bank transfer payout

Send to 40+ Tanzanian banks. Snippe handles the routing — you supply the bank code, account number, and recipient name.

### Request

```json
{
  "amount": 5000,
  "channel": "bank",
  "recipient_bank": "ABSA",
  "recipient_account": "0200000000",
  "recipient_name": "Recipient Name",
  "narration": "Invoice payment INV-2026-001",
  "webhook_url": "https://yoursite.com/webhooks/snippe",
  "metadata": { "invoice_id": "INV-2026-001" }
}
```

### Required fields

- `amount` — integer ≥ 5000 TZS
- `channel` — `"bank"`
- `recipient_bank` — one of the supported bank codes (see below)
- `recipient_account` — the destination account number
- `recipient_name` — must match the account holder's name on file at the bank, or the transfer may be rejected

Optional:
- `narration` — shows on the bank statement
- `webhook_url`, `metadata`

The response shape is the same as mobile money payouts, except `channel` is `{"type": "bank", ...}`.

## Supported bank codes

Pass these exact strings as `recipient_bank`. Common ones:

| Code       | Bank                                          |
| ---------- | --------------------------------------------- |
| `ABSA`     | Absa Bank Tanzania                            |
| `ACCESS`   | Access Bank Tanzania                          |
| `AKIBA`    | Akiba Commercial Bank                         |
| `AMANA`    | Amana Bank                                    |
| `AZANIA`   | Azania Bank                                   |
| `BARODA`   | Bank of Baroda                                |
| `BOA`      | Bank of Africa                                |
| `CITI`     | Citibank Tanzania                             |
| `CRDB`     | CRDB Bank                                     |
| `DTB`      | Diamond Trust Bank                            |
| `ECOBANK`  | Ecobank Tanzania                              |
| `EQUITY`   | Equity Bank Tanzania                          |
| `EXIM`     | Exim Bank Tanzania                            |
| `FNB`      | First National Bank Tanzania                  |
| `HABIB`    | Habib African Bank                            |
| `IMBANK`   | I&M Bank                                      |
| `KCB`      | Kenya Commercial Bank (KCB) Tanzania          |
| `NBC`      | National Bank of Commerce                     |
| `NCBA`     | NCBA Bank Tanzania                            |
| `NMB`      | National Microfinance Bank                    |
| `PBZ`      | People's Bank of Zanzibar                     |
| `SCB`      | Standard Chartered Bank Tanzania              |
| `STANBIC`  | Stanbic Bank Tanzania                         |
| `TCB`      | Tanzania Commercial Bank                      |
| `UBA`      | United Bank for Africa (UBA) Tanzania         |

This list covers the most-used banks in Tanzania but isn't exhaustive. For the full, current list fetch `https://snippe.sh/docs/2026-01-25/disbursements/bank-transfer.mdx` — the page includes every supported code.

If the user passes an unknown bank code, the API returns a `400 validation_error` with a message indicating the bank isn't supported. Validate against this list on your side first for better error messages to end users.
