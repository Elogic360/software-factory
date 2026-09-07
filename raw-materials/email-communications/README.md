# Raw Material: Email & Notification Core

**Category:** Communications | **Status:** REFERENCE | **Language:** Python

## What This Provides

A complete, credential-free notification layer: SMTP email, template-based
HTML email (Jinja2), webhook firing, Slack messaging, and a factory event
broadcaster that fans out to all configured channels simultaneously.

No vendor lock-in. Zero hardcoded credentials. All config via env vars.

## Key Functions

| Function | Description |
|---|---|
| `send_email(to, subject, body)` | SMTP email sender |
| `send_template(template_name, context, to)` | Jinja2 template-based email |
| `send_webhook_notification(url, payload)` | Generic JSON webhook |
| `send_slack_message(message, channel)` | Slack incoming webhook |
| `notify_factory_event(event_type, details)` | Fan-out to all channels |

## Required Environment Variables

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@email.com
SMTP_PASS=your_app_password
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
FACTORY_WEBHOOK_URL=https://your-webhook.example.com/events
FACTORY_ALERT_EMAIL=alerts@yourcompany.com
```

## Quick Start

```python
from raw_materials.email_communications.email_core import send_slack_message, notify_factory_event

# Simple Slack notification
send_slack_message("🚀 Deployment started for project-x")

# Full event broadcast (Slack + webhook)
notify_factory_event("project.deployed", {"project": "integral-market", "env": "production"})
```

## Wiring into Factory Events

```python
from core.event_bus import FactoryEventBus
from raw_materials.email_communications.email_core import notify_factory_event

bus = FactoryEventBus()
bus.subscribe("gate.failed", lambda e: notify_factory_event("gate.failed", e, channels=["slack","email"]))
```
