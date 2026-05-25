# SKILL: Observability Engineer
## Domain: Structured Logging, Metrics, Tracing, Alerting

**Activation triggers:** logging setup, metrics endpoint, Prometheus, Grafana,
OpenTelemetry, distributed tracing, structured logs, health dashboard, alerting
rules, performance monitoring.

---

## Structured Logging Standard

```python
# integral-expert-backend/app/core/logging.py
import logging
import json
import sys
from datetime import datetime, timezone

class JSONFormatter(logging.Formatter):
    """Emit every log line as a single JSON object — Grafana Loki compatible."""

    RESERVED = {"message", "asctime", "levelname", "name", "pathname", "lineno"}

    def format(self, record: logging.LogRecord) -> str:
        base = {
            "ts":      datetime.now(timezone.utc).isoformat(),
            "level":   record.levelname,
            "logger":  record.name,
            "msg":     record.getMessage(),
            "file":    f"{record.pathname}:{record.lineno}",
        }
        # Merge extra fields (structured context)
        extra = {k: v for k, v in record.__dict__.items() if k not in self.RESERVED and not k.startswith("_")}
        if record.exc_info:
            extra["exc"] = self.formatException(record.exc_info)
        return json.dumps({**base, **extra})

def setup_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logging.basicConfig(level=level, handlers=[handler], force=True)

# Usage throughout the app:
# logger.info("Trade synced", extra={"account_id": str(account_id), "trade_count": len(trades)})
```

---

## Prometheus Metrics

```python
# app/core/metrics.py
from prometheus_client import Counter, Histogram, Gauge, REGISTRY
from prometheus_client.openmetrics.exposition import generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

# Request metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code", "service"],
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint", "service"],
    buckets=[.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10],
)

# Business metrics
TRADES_SYNCED = Counter(
    "trades_synced_total",
    "Total trades synced from brokers",
    ["account_id", "broker_type"],
)
ACTIVE_WS_CONNECTIONS = Gauge(
    "active_ws_connections",
    "Currently active WebSocket connections",
)
SIGNAL_EXECUTIONS = Counter(
    "copy_signal_executions_total",
    "Copy trading signal executions",
    ["status"],  # success | blocked_risk | blocked_symbol | failed
)

@app.get("/metrics", include_in_schema=False)
async def metrics():
    return Response(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)
```

---

## Metrics Middleware

```python
# app/core/metrics_middleware.py
import time
from fastapi import Request
from app.core.metrics import REQUEST_COUNT, REQUEST_LATENCY

async def metrics_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start

    # Normalize path (replace UUIDs with {id} to avoid cardinality explosion)
    path = _normalize_path(request.url.path)

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=path,
        status_code=response.status_code,
        service="expert-backend",
    ).inc()
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=path,
        service="expert-backend",
    ).observe(duration)

    return response

def _normalize_path(path: str) -> str:
    import re
    # Replace UUIDs with {id}
    path = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '{id}', path)
    # Replace numeric IDs
    path = re.sub(r'/\d+', '/{id}', path)
    return path
```

---

## OpenTelemetry Tracing (Distributed)

```python
# app/core/tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

def setup_tracing(app, service_name: str) -> None:
    if not settings.OTEL_EXPORTER_OTLP_ENDPOINT:
        return   # skip tracing in dev unless configured

    provider = TracerProvider()
    exporter = OTLPSpanExporter(endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    FastAPIInstrumentor.instrument_app(app)
    SQLAlchemyInstrumentor().instrument(engine=engine)

# Custom span for business events
tracer = trace.get_tracer("integral-market")

async def route_signal_with_tracing(signal: ProviderSignal) -> None:
    with tracer.start_as_current_span("route_copy_signal") as span:
        span.set_attribute("provider_id", str(signal.provider_id))
        span.set_attribute("symbol", signal.symbol)
        span.set_attribute("lot_size", signal.lot_size)
        await SignalService.route_signal(signal)
```

---

## Grafana Dashboard Template (JSON)

```yaml
# docker-compose.yml snippet — Grafana + Prometheus + Loki stack
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    ports: ["9090:9090"]

  grafana:
    image: grafana/grafana:latest
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD}
    volumes:
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources
    ports: ["3001:3000"]

  loki:
    image: grafana/loki:latest
    ports: ["3100:3100"]
```

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: market-backend
    static_configs:
      - targets: ['market-backend:8000']
    metrics_path: /metrics

  - job_name: expert-backend
    static_configs:
      - targets: ['expert-backend:8002']
    metrics_path: /metrics
```

---

## Alert Rules (Prometheus Alertmanager)

```yaml
# monitoring/alerts.yml
groups:
  - name: integral-market
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status_code=~"5.."}[5m]) > 0.05
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Error rate > 5% on {{ $labels.service }}"

      - alert: HighLatency
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 3m
        labels:
          severity: warning
        annotations:
          summary: "p99 latency > 2s on {{ $labels.service }}"

      - alert: TradesSyncStopped
        expr: rate(trades_synced_total[30m]) == 0
        for: 30m
        labels:
          severity: warning
        annotations:
          summary: "No trades synced in 30 minutes — MT5 worker may be down"
```

---

## Anti-Patterns

```
✗ Using print() instead of structured logger (unqueryable in Loki)
✗ Logging PII — user emails, IP addresses, account credentials
✗ High-cardinality metric labels (e.g., user_id per request → OOM)
✗ Missing /metrics endpoint (no visibility into service health)
✗ No latency histogram (counter alone can't detect P99 spikes)
✗ Tracing every DB query in production without sampling (overhead)
✗ Logging exceptions without exc_info=True (stack trace lost)
✗ Alert on noisy metrics with no for: duration (alert storms)
```
