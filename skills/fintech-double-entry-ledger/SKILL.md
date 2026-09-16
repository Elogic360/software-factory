---
name: fintech-double-entry-ledger
description: Double-entry accounting for fintech applications — journal entries, balance invariants, reconciliation, and financial precision
version: "1.0.0"
domain: fintech
tags: [ledger, accounting, double-entry, journal, reconciliation, decimal, fintech, payments]
contributed_by: trinance-engineering
---

# SKILL: Fintech Engineer — Double-Entry Ledger

## Domain: Financial Accounting for Blockchain/Payments Applications

**Activation triggers:** journal entry, ledger account, balance calculation, financial reconciliation, money amount, Decimal precision, credit/debit, chart of accounts, settlement, audit trail, idempotency.

---

## Absolute Financial Rules

```
NEVER:
  - Use float for money (causes rounding errors — use Decimal)
  - Store amounts in DB as FLOAT or DOUBLE PRECISION (use NUMERIC)
  - Accept unbalanced journal entries (DR ≠ CR)
  - Modify existing journal entries (append-only ledger)
  - Credit balances from unverified provider state
  - Use blockchain balance as the canonical application balance
  - Silently correct financial discrepancies

ALWAYS:
  - Use Decimal in Python
  - Use NUMERIC(precision, scale) in PostgreSQL — never FLOAT
  - Enforce DR = CR on every journal entry before persisting
  - Record every financial event as a journal entry
  - Reconcile application ledger against external provider state
  - Create RECONCILIATION_REQUIRED records for discrepancies
  - Store idempotency keys for all financial operations
```

## Amount Type Rules

```python
from decimal import Decimal, ROUND_HALF_UP

# CORRECT
amount = Decimal("100.50")
fee = Decimal("0.000000001")  # Sub-satoshi precision for internal accounting

# WRONG
amount = 100.50      # float — NEVER
amount = 100         # int is OK only for satoshis (already atomic)

# PostgreSQL column
from sqlalchemy import Numeric
amount: Mapped[Decimal] = mapped_column(Numeric(precision=36, scale=18))
# precision=36 handles values up to 10^18 BTC
# scale=18 supports sub-satoshi precision for stablecoins
```

## Double-Entry Invariant

```python
# EVERY journal entry MUST satisfy:
sum(DR lines) == sum(CR lines)

# Example: User deposits 100 USDC
# DR User_USDC_Asset = 100       (user's asset increases)
# CR Trinance_USDC_Custody = 100 (liability to user increases)
# BALANCED: 100 DR = 100 CR ✓

# Example: Fee collection
# DR User_BTC_Asset = 0.0001     (user balance decreases)
# CR Trinance_Fee_Revenue = 0.0001 (fee revenue increases)
# BALANCED: 0.0001 DR = 0.0001 CR ✓
```

## SQLAlchemy Models

```python
class LedgerAccount(Base):
    __tablename__ = "ledger_accounts"
    name: Mapped[str]
    account_type: Mapped[str]  # ASSET | LIABILITY | EQUITY | REVENUE | EXPENSE
    currency: Mapped[str]       # BTC, USDC, TRUSD, TZS
    network: Mapped[Optional[str]]  # Bitcoin, Stellar, Lightning
    owner_id: Mapped[Optional[str]]  # user_id for user accounts, NULL for system

class JournalEntry(Base):
    __tablename__ = "journal_entries"
    description: Mapped[str]
    entry_type: Mapped[str]  # DEPOSIT | WITHDRAWAL | TRANSFER | FEE | MINT | BURN
    reference_id: Mapped[Optional[str]]  # payment_id, txid, order_id
    total_debits: Mapped[Decimal] = mapped_column(Numeric(36, 18))
    total_credits: Mapped[Decimal] = mapped_column(Numeric(36, 18))

    @property
    def is_balanced(self) -> bool:
        return self.total_debits == self.total_credits

class JournalLine(Base):
    __tablename__ = "journal_lines"
    entry_id: Mapped[str]
    account_id: Mapped[str]
    amount: Mapped[Decimal] = mapped_column(Numeric(36, 18))
    direction: Mapped[str]  # "DR" or "CR" ONLY
```

## Ledger Service Pattern

```python
class LedgerService:
    async def create_journal_entry(
        self,
        description: str,
        lines: list[dict],  # [{"account_id": ..., "direction": "DR"|"CR", "amount": Decimal}]
        reference_id: Optional[str] = None,
        entry_type: str = "GENERAL",
    ) -> JournalEntry:
        # 1. Validate: amount must be Decimal
        # 2. Calculate totals
        total_dr = sum(l["amount"] for l in lines if l["direction"] == "DR")
        total_cr = sum(l["amount"] for l in lines if l["direction"] == "CR")
        # 3. REJECT if not balanced
        if total_dr != total_cr:
            raise UnbalancedEntryError(total_dr, total_cr)
        # 4. Persist atomically
        # 5. Return entry
```

## Chart of Accounts Pattern

```python
ACCOUNT_TYPES = {
    # User accounts (one per user per asset)
    "USER_ASSET": "ASSET",        # DR increases balance

    # Trinance system accounts
    "CUSTODY": "LIABILITY",       # CR increases (Trinance owes user)
    "FEE_REVENUE": "REVENUE",     # CR increases (Trinance earns)
    "RESERVE": "ASSET",           # DR increases (backing TRUSD)
    "TRUSD_LIABILITY": "LIABILITY", # CR increases (outstanding TRUSD)

    # Operational
    "TRANSIT": "LIABILITY",       # Temporary holding during settlement
    "SUSPENSE": "LIABILITY",      # Unidentified payments
}
```

## Reconciliation Pattern

```python
async def reconcile_payment(payment_id: str):
    """Compare internal ledger vs provider state."""
    payment = await payment_repo.get(payment_id)
    provider_status = await tunzaa.get_payment(payment.provider_reference)

    internal_succeeded = payment.status == PaymentStatus.SUCCEEDED
    provider_succeeded = provider_status.status == "COMPLETED"

    if internal_succeeded and not provider_succeeded:
        # CRITICAL: We credited user but provider shows not completed
        await create_reconciliation_alert(payment_id, "OVERCREDIT")

    if provider_succeeded and not internal_succeeded:
        # Provider succeeded but we didn't credit
        await payment_service.transition(payment_id, PaymentStatus.RECONCILIATION_REQUIRED,
            reason="Provider succeeded but internal not updated")
```

## Idempotency for Financial Operations

```python
async def process_payment_with_idempotency(
    idempotency_key: str,
    payment_data: dict,
) -> Payment:
    # 1. Check if already processed
    existing = await idempotency_repo.get(idempotency_key)
    if existing:
        return await payment_repo.get(existing.resource_id)

    # 2. Process (atomic — use DB transaction)
    async with session.begin():
        payment = await payment_service.create(payment_data)
        await idempotency_repo.create(idempotency_key, payment.id)

    return payment
```
