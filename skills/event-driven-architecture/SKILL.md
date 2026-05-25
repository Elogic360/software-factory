# SKILL: Event-Driven Architecture Engineer
## Domain: Domain Events, Event Bus, CQRS, Saga Pattern

**Activation triggers:** domain event, event bus, pub/sub architecture, CQRS,
saga, event sourcing, async workflow, decoupled service communication, Redis
streams, background event processing.

---

## Event-Driven Design Principles for Integral Market

```
WHEN to use events (not direct service calls):
  ✅ Trade executed → update journal, notify subscribers, update analytics
  ✅ User subscribed to provider → send welcome notification, log to audit
  ✅ Provider signal generated → fan-out to all active subscribers
  ✅ Account connected → trigger initial sync
  ✅ Payment processed → upgrade user role, send receipt

WHEN NOT to use events:
  ✗ Authentication (synchronous, needs immediate response)
  ✗ Read queries (synchronous, needs immediate data)
  ✗ Operations requiring transactional consistency with the emitter
```

---

## Domain Event Schema

```python
# app/core/events.py
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import uuid

@dataclass
class DomainEvent:
    """Base class for all domain events."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = field(default="")        # e.g., "TradeExecuted"
    aggregate_id: str = field(default="")      # e.g., trade UUID
    aggregate_type: str = field(default="")    # e.g., "Trade"
    payload: dict = field(default_factory=dict)
    occurred_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    correlation_id: str | None = None          # trace across services

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "payload": self.payload,
            "occurred_at": self.occurred_at,
            "correlation_id": self.correlation_id,
        }

# Specific events
@dataclass
class TradeExecutedEvent(DomainEvent):
    event_type: str = "TradeExecuted"
    aggregate_type: str = "Trade"

@dataclass
class ProviderSignalEmittedEvent(DomainEvent):
    event_type: str = "ProviderSignalEmitted"
    aggregate_type: str = "ProviderSignal"

@dataclass
class UserSubscribedToProviderEvent(DomainEvent):
    event_type: str = "UserSubscribedToProvider"
    aggregate_type: str = "CopySubscription"
```

---

## Redis Streams Event Bus

```python
# app/core/event_bus.py
import json
import asyncio
import logging
from typing import Callable, Awaitable
import aioredis

logger = logging.getLogger(__name__)

EventHandler = Callable[[dict], Awaitable[None]]

class EventBus:
    """Redis Streams-backed event bus. Durable, at-least-once delivery."""

    def __init__(self, redis: aioredis.Redis):
        self.redis = redis
        self._handlers: dict[str, list[EventHandler]] = {}

    async def publish(self, event: "DomainEvent") -> None:
        """Publish event to its stream. Non-blocking."""
        stream = f"events:{event.aggregate_type.lower()}"
        await self.redis.xadd(
            stream,
            event.to_dict(),
            maxlen=100_000,    # keep last 100k events per stream
        )
        logger.info("Event published", extra={
            "event_type": event.event_type,
            "aggregate_id": event.aggregate_id,
            "stream": stream,
        })

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """Register a handler for an event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    async def start_consumer(
        self,
        stream: str,
        group: str,
        consumer: str,
        batch_size: int = 10,
    ) -> None:
        """Long-running consumer loop — run as background task."""
        # Create consumer group if needed
        try:
            await self.redis.xgroup_create(stream, group, id="0", mkstream=True)
        except aioredis.ResponseError:
            pass   # group already exists

        while True:
            try:
                messages = await self.redis.xreadgroup(
                    groupname=group,
                    consumername=consumer,
                    streams={stream: ">"},   # ">" = undelivered messages
                    count=batch_size,
                    block=5000,              # block 5s if no messages
                )
                for stream_name, events in (messages or []):
                    for event_id, data in events:
                        await self._dispatch(event_id, data, stream_name, group)
            except Exception as exc:
                logger.exception("Event consumer error", extra={"stream": stream, "error": str(exc)})
                await asyncio.sleep(5)   # backoff before retry

    async def _dispatch(self, event_id: str, data: dict, stream: str, group: str) -> None:
        event_type = data.get("event_type", "")
        handlers = self._handlers.get(event_type, [])
        for handler in handlers:
            try:
                await handler(data)
                await self.redis.xack(stream, group, event_id)
            except Exception as exc:
                logger.exception("Handler failed", extra={
                    "event_type": event_type,
                    "event_id": event_id,
                    "error": str(exc),
                })
                # Do NOT ack — message will be redelivered (at-least-once)
```

---

## Signal Fan-Out Saga (Copy Trading)

```python
# Signal routed to all subscribers — fan-out pattern
# integral-expert-backend/app/sagas/signal_routing_saga.py

class SignalRoutingSaga:
    """
    Saga for routing a provider signal to all active subscribers.
    Each step is independently retryable.
    """

    async def execute(self, signal: ProviderSignal, db: AsyncSession) -> None:
        subscriptions = await self._get_active_subscriptions(signal.provider_id, db)

        for subscription in subscriptions:
            try:
                await self._route_to_subscriber(signal, subscription, db)
            except Exception as exc:
                # Log and continue — one subscriber failure must not block others
                logger.exception("Subscriber routing failed", extra={
                    "subscription_id": str(subscription.id),
                    "signal_id": str(signal.id),
                    "error": str(exc),
                })

    async def _route_to_subscriber(
        self,
        signal: ProviderSignal,
        subscription: CopySubscription,
        db: AsyncSession,
    ) -> None:
        risk_engine = RiskEngine()
        allowed, reason = await risk_engine.check_limits(subscription, signal)

        if not allowed:
            await self._log_execution(subscription.id, signal.id, "blocked", reason, db)
            return

        # Execute on subscriber's broker
        adapter = await BrokerRegistry.instance().get(str(subscription.account_id), db)
        result = await adapter.place_order(
            symbol=signal.symbol,
            direction=signal.direction,
            volume=signal.lot_size * (subscription.copy_ratio or 1.0),
        )

        status = "success" if result.get("ticket") else "failed"
        await self._log_execution(subscription.id, signal.id, status, "", db)

    async def _log_execution(self, sub_id, signal_id, status, reason, db):
        log = ExecutionLog(
            subscription_id=sub_id,
            signal_id=signal_id,
            status=status,
            failure_reason=reason or None,
        )
        db.add(log)
        await db.commit()
```

---

## Anti-Patterns

```
✗ Synchronous fan-out in request path (blocks for all subscribers)
✗ Losing events when consumer crashes (use Redis Streams with consumer groups)
✗ Acknowledging before processing (ack after successful handler)
✗ Events with massive payloads (store reference, not full data)
✗ No correlation_id for tracing across services
✗ One subscriber's failure blocking others (always isolate per-subscriber)
✗ Using pub/sub (lossy) for business-critical events (use Streams)
✗ Infinite retry without dead-letter queue for poison messages
```
