---
name: blockchain-lightning-network
description: Lightning Network development — LND/CLN adapters, invoice management, channel operations, routing, and Polar integration
version: "1.0.0"
domain: blockchain
tags: [lightning, lnd, cln, channels, invoices, payments, routing, polar, htlc, liquidity]
contributed_by: trinance-engineering
---

# SKILL: Blockchain Engineer — Lightning Network

## Domain: Lightning Network Integration for Fintech Applications

**Activation triggers:** Lightning invoice, LND gRPC, Core Lightning JSON-RPC, channel management, routing, liquidity, HTLC, Polar lightning nodes, Lightning payment, msats, satoshis.

---

## Amount Units — Critical

```python
# Lightning uses millisatoshis (msats) internally
# 1 satoshi = 1000 msats
# NEVER use float — use integer msats or Decimal BTC

MSATS_PER_SAT = 1000
SATS_PER_BTC = 100_000_000

def btc_to_msats(btc: Decimal) -> int:
    return int(btc * SATS_PER_BTC * MSATS_PER_SAT)

def msats_to_btc(msats: int) -> Decimal:
    return Decimal(msats) / (SATS_PER_BTC * MSATS_PER_SAT)

def sats_to_msats(sats: int) -> int:
    return sats * MSATS_PER_SAT
```

## Architecture Pattern

```
Frontend (NEVER accesses LND/CLN directly)
    ↓
Trinance API
    ↓
LightningService
    ↓
LightningGateway (interface)
    ↓
LNDAdapter | CLNAdapter (implementation)
    ↓
LND gRPC | CLN JSON-RPC
```

## Gateway Interface Template

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class LightningInvoice:
    payment_hash: str
    payment_request: str    # BOLT11 encoded invoice
    amount_msats: int
    expiry_seconds: int
    created_at: int
    memo: str

@dataclass
class LightningPayment:
    payment_hash: str
    payment_preimage: Optional[str]
    amount_msats: int
    fee_msats: int
    status: str  # UNKNOWN | IN_FLIGHT | SUCCEEDED | FAILED
    failure_reason: Optional[str]

class LightningGateway(ABC):
    @abstractmethod
    async def create_invoice(
        self,
        amount_msats: int,
        memo: str,
        expiry_seconds: int = 3600,
    ) -> LightningInvoice: ...

    @abstractmethod
    async def pay_invoice(
        self,
        payment_request: str,
        max_fee_msats: Optional[int] = None,
    ) -> LightningPayment: ...

    @abstractmethod
    async def get_payment(self, payment_hash: str) -> LightningPayment: ...

    @abstractmethod
    async def get_node_info(self) -> dict: ...

    @abstractmethod
    async def list_channels(self) -> list[dict]: ...
```

## LND Adapter (via gRPC)

```python
# Install: pip install grpcio lnrpc
# Generate protobufs or use lnd-grpc library

class LNDAdapter(LightningGateway):
    def __init__(self, host: str, macaroon_path: str, cert_path: str):
        # macaroon: invoice.macaroon (NOT admin.macaroon — principle of least privilege)
        # cert: tls.cert
        self._host = host
        self._macaroon_path = macaroon_path
        self._cert_path = cert_path

    async def create_invoice(self, amount_msats: int, memo: str, ...) -> LightningInvoice:
        # Use invoice.AddInvoice gRPC call
        # Return structured LightningInvoice

    async def pay_invoice(self, payment_request: str, ...) -> LightningPayment:
        # Use router.SendPaymentV2 (streaming)
        # Handle IN_FLIGHT, SUCCEEDED, FAILED
        # NEVER return SUCCEEDED without payment_preimage
```

## Failure Handling (Critical)

```python
# Lightning payments can fail at many levels:
# 1. No route found
# 2. Insufficient channel balance
# 3. Remote node offline
# 4. HTLC timeout
# 5. Fee limit exceeded

async def pay_with_retry(payment_request: str, max_retries: int = 3):
    for attempt in range(max_retries):
        result = await lightning.pay_invoice(payment_request)
        if result.status == "SUCCEEDED":
            return result
        if result.failure_reason in ("ROUTE_NOT_FOUND", "INSUFFICIENT_BALANCE"):
            raise LightningPaymentError(result.failure_reason)
        # Exponential backoff for transient failures
        await asyncio.sleep(2 ** attempt)
    raise LightningPaymentError("Max retries exceeded")
```

## Polar Development Setup

```bash
# Polar creates local regtest Bitcoin + LND + CLN nodes
# After Polar starts, get connection details from UI:

# LND REST endpoint (Polar default): http://127.0.0.1:8080
# LND gRPC endpoint: 127.0.0.1:10009
# Macaroon: ~/.polar/networks/<id>/volumes/lnd/alice/data/chain/bitcoin/regtest/admin.macaroon
# TLS cert: ~/.polar/networks/<id>/volumes/lnd/alice/tls.cert

# For CLN:
# RPC socket: ~/.polar/networks/<id>/volumes/cln/bob/run/lightning-rpc
```

## Invoice Lifecycle

```
CREATED (invoice generated, waiting for payment)
    ↓
PENDING (payment in flight — do NOT credit yet)
    ↓
SETTLED (preimage received — SAFE to credit ledger)
    ↓
EXPIRED (not paid within expiry)
    ↓
CANCELLED (manually cancelled)

RULE: Only credit the ledger when status == SETTLED
      AND payment_preimage is present (cryptographic proof of payment)
```

## Security Rules

```
□ Use invoice.macaroon, NOT admin.macaroon (principle of least privilege)
□ Never expose LND/CLN RPC to the internet
□ Verify payment_preimage before crediting user balance
□ Set invoice expiry (default 1 hour, reduce for high-value)
□ Monitor for duplicate payment_hash (should be impossible but verify)
□ Max fee limits on outbound payments
□ Never send sats to unverified addresses
□ Channel backup strategy (Static Channel Backups)
```
