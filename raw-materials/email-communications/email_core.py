"""
Universal Email & Notification Core — Reference Implementation
Software Factory Raw Material: email-communications

Provides SMTP email, Jinja2 template rendering, webhook notifications,
and Slack messaging. All credentials read from environment variables.
"""
from __future__ import annotations
import json
import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, Optional
import urllib.request


# ── Configuration ─────────────────────────────────────────────────────────────

def _smtp_config() -> Dict[str, Any]:
    return {
        "host": os.environ.get("SMTP_HOST", "smtp.gmail.com"),
        "port": int(os.environ.get("SMTP_PORT", "587")),
        "user": os.environ.get("SMTP_USER", ""),
        "password": os.environ.get("SMTP_PASS", ""),
        "from_addr": os.environ.get("SMTP_FROM", os.environ.get("SMTP_USER", "")),
        "use_tls": os.environ.get("SMTP_TLS", "true").lower() == "true",
    }


# ── SMTP Email ────────────────────────────────────────────────────────────────

def send_email(
    to: str,
    subject: str,
    body: str,
    html_body: Optional[str] = None,
    from_addr: Optional[str] = None,
    smtp_host: Optional[str] = None,
    smtp_port: Optional[int] = None,
    smtp_user: Optional[str] = None,
    smtp_pass: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Send an email via SMTP. Reads config from env vars by default.

    Env vars: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_FROM, SMTP_TLS

    Returns:
        dict with keys: success (bool), message_id (str), error (str or None)
    """
    cfg = _smtp_config()
    host = smtp_host or cfg["host"]
    port = smtp_port or cfg["port"]
    user = smtp_user or cfg["user"]
    password = smtp_pass or cfg["password"]
    sender = from_addr or cfg["from_addr"]

    if not sender:
        return {"success": False, "error": "SMTP_FROM or SMTP_USER must be set"}
    if not user or not password:
        return {"success": False, "error": "SMTP_USER and SMTP_PASS must be set"}

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to
    msg.attach(MIMEText(body, "plain"))
    if html_body:
        msg.attach(MIMEText(html_body, "html"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(host, port) as server:
            if cfg["use_tls"]:
                server.starttls(context=context)
            server.login(user, password)
            server.sendmail(sender, [to], msg.as_string())
        return {"success": True, "message_id": msg.get("Message-ID"), "error": None}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ── Template Email ────────────────────────────────────────────────────────────

def send_template(
    template_name: str,
    context: Dict[str, Any],
    to: str,
    subject: Optional[str] = None,
    templates_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Send a Jinja2 template-based email.

    Args:
        template_name: filename under templates_dir (e.g. 'welcome.html')
        context: variables to render into the template
        to: recipient email address
        subject: email subject (falls back to template variable 'subject')
        templates_dir: path to templates directory (default: ./email_templates)

    Returns:
        Same as send_email()
    """
    try:
        from jinja2 import Environment, FileSystemLoader  # type: ignore
    except ImportError:
        return {"success": False, "error": "pip install jinja2 to use send_template"}

    tdir = templates_dir or os.path.join(os.path.dirname(__file__), "email_templates")
    env = Environment(loader=FileSystemLoader(tdir), autoescape=True)
    try:
        template = env.get_template(template_name)
    except Exception as e:
        return {"success": False, "error": f"Template not found: {e}"}

    rendered = template.render(**context)
    subject = subject or context.get("subject", f"Message from {_smtp_config()['from_addr']}")
    return send_email(to=to, subject=subject, html_body=rendered,
                      body=f"This email requires HTML. Subject: {subject}")


# ── Webhook Notification ──────────────────────────────────────────────────────

def send_webhook_notification(
    url: str,
    payload: Dict[str, Any],
    method: str = "POST",
    timeout: int = 10,
    headers: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Send a JSON webhook notification to any URL.

    Args:
        url: webhook endpoint URL
        payload: dict to send as JSON body
        method: HTTP method (default POST)
        timeout: request timeout in seconds
        headers: optional additional headers

    Returns:
        dict with: success (bool), status_code (int), response (str), error (str or None)
    """
    body = json.dumps(payload).encode("utf-8")
    req_headers = {"Content-Type": "application/json", "User-Agent": "software-factory/1.0"}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, data=body, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {
                "success": True,
                "status_code": resp.status,
                "response": resp.read(500).decode("utf-8", errors="replace"),
                "error": None,
            }
    except Exception as e:
        return {"success": False, "status_code": None, "response": None, "error": str(e)}


# ── Slack Notification ────────────────────────────────────────────────────────

def send_slack_message(
    message: str,
    channel: Optional[str] = None,
    webhook_url: Optional[str] = None,
    icon_emoji: str = ":factory:",
    username: str = "Software Factory",
) -> Dict[str, Any]:
    """
    Send a message to Slack via incoming webhook.

    Env vars: SLACK_WEBHOOK_URL, SLACK_CHANNEL

    Args:
        message: plain-text message to send (supports Slack mrkdwn)
        channel: Slack channel override (e.g. '#alerts')
        webhook_url: override SLACK_WEBHOOK_URL env var
        icon_emoji: bot icon emoji
        username: display name for the bot message

    Returns:
        dict with: success (bool), error (str or None)
    """
    url = webhook_url or os.environ.get("SLACK_WEBHOOK_URL")
    if not url:
        return {"success": False, "error": "SLACK_WEBHOOK_URL env var not set"}
    ch = channel or os.environ.get("SLACK_CHANNEL", "#general")
    payload = {"text": message, "channel": ch, "icon_emoji": icon_emoji, "username": username}
    result = send_webhook_notification(url, payload)
    return {"success": result["success"], "error": result.get("error")}


# ── Factory Event Notifier ────────────────────────────────────────────────────

def notify_factory_event(
    event_type: str,
    details: Dict[str, Any],
    channels: Optional[list] = None,
) -> Dict[str, Any]:
    """
    Broadcast a factory lifecycle event to all configured channels.

    Args:
        event_type: e.g. 'project.deployed', 'gate.failed', 'build.success'
        details: event payload
        channels: list of channel types to use: ['slack', 'webhook', 'email']
                  defaults to all available

    Returns:
        dict of channel → result
    """
    channels = channels or ["slack", "webhook"]
    results = {}
    message = f"[{event_type.upper()}] {json.dumps(details, default=str)}"

    if "slack" in channels:
        results["slack"] = send_slack_message(message)

    if "webhook" in channels:
        webhook_url = os.environ.get("FACTORY_WEBHOOK_URL")
        if webhook_url:
            results["webhook"] = send_webhook_notification(
                webhook_url, {"event": event_type, "details": details})
        else:
            results["webhook"] = {"success": False, "error": "FACTORY_WEBHOOK_URL not set"}

    if "email" in channels:
        alert_email = os.environ.get("FACTORY_ALERT_EMAIL")
        if alert_email:
            results["email"] = send_email(
                to=alert_email, subject=f"[Factory] {event_type}", body=message)
        else:
            results["email"] = {"success": False, "error": "FACTORY_ALERT_EMAIL not set"}

    return results
