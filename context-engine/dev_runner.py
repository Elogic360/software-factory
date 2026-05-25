#!/usr/bin/env python3
"""
dev_runner.py — Integral Market Full-Stack Dev Runner

Launches all services (PostgreSQL check, Redis check, Market Backend,
Expert Backend via Podman/Docker, IMI Backend, Frontend), streams logs
from all of them, and provides a health check endpoint.

Usage:
    python3 dev_runner.py --start-all             # launch all services
    python3 dev_runner.py --start-all --follow    # launch + stream logs
    python3 dev_runner.py --start-all --watch     # launch + auto-restart on failure
    python3 dev_runner.py --health                # check all services
    python3 dev_runner.py --stop-all              # kill all services
    python3 dev_runner.py --logs                  # stream existing logs only
"""

from __future__ import annotations

import argparse
import os
import shutil
import signal
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import urllib.request
import urllib.error

ROOT = Path(__file__).parent.parent.parent  # project root

# ── ANSI colours ──────────────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
BLUE   = "\033[34m"
MAGENTA= "\033[35m"
CYAN   = "\033[36m"
WHITE  = "\033[37m"

def ts() -> str:
    return datetime.now(timezone.utc).strftime("%H:%M:%S")

def ok(msg: str)   -> None: print(f"{GREEN}✅ {msg}{RESET}")
def err(msg: str)  -> None: print(f"{RED}❌ {msg}{RESET}")
def warn(msg: str) -> None: print(f"{YELLOW}⚠️  {msg}{RESET}")
def info(msg: str) -> None: print(f"{CYAN}ℹ️  {msg}{RESET}")
def step(msg: str) -> None: print(f"{BOLD}{BLUE}── {msg}{RESET}")


# ── Service definitions ───────────────────────────────────────────────────────

@dataclass
class ServiceConfig:
    name:      str
    color:     str
    port:      int
    log_file:  str
    health_url: str
    start_cmd: list[str]
    cwd:       Path
    env_extra: dict[str, str] = field(default_factory=dict)
    use_container: bool = False   # Expert backend uses Podman/Docker
    container_name: str = ""


SERVICES: list[ServiceConfig] = [
    ServiceConfig(
        name       = "Market",
        color      = BLUE,
        port       = 8000,
        log_file   = "/tmp/market-backend.log",
        health_url = "http://localhost:8000/health",
        start_cmd  = [
            "bash", "-c",
            "source venv/bin/activate && "
            "uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
        ],
        cwd        = ROOT / "integral-market-backend",
    ),
    ServiceConfig(
        name           = "Expert",
        color          = MAGENTA,
        port           = 8002,
        log_file       = "/tmp/expert-backend.log",
        health_url     = "http://localhost:8002/health",
        start_cmd      = [],   # handled by _start_container()
        cwd            = ROOT / "integral-expert-backend",
        use_container  = True,
        container_name = "integral-expert-backend",
    ),
    ServiceConfig(
        name      = "IMI",
        color     = YELLOW,
        port      = 8003,
        log_file  = "/tmp/imi-backend.log",
        health_url= "http://localhost:8003/health",
        start_cmd = [
            "bash", "-c",
            "source venv/bin/activate && "
            "uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload"
        ],
        cwd       = ROOT / "integral-market-intelligence",
    ),
    ServiceConfig(
        name      = "Frontend",
        color     = CYAN,
        port      = 5173,
        log_file  = "/tmp/frontend.log",
        health_url= "http://localhost:5173",
        start_cmd = ["pnpm", "dev"],
        cwd       = ROOT / "app",
    ),
]


# ── Infrastructure checks ─────────────────────────────────────────────────────

def check_postgres() -> bool:
    result = subprocess.run(
        ["pg_isready", "-h", "localhost", "-p", "5432"],
        capture_output=True, text=True
    )
    return result.returncode == 0


def check_redis() -> bool:
    result = subprocess.run(
        ["redis-cli", "-p", "6380", "ping"],
        capture_output=True, text=True, timeout=3
    )
    return "PONG" in result.stdout


def check_http(url: str, timeout: int = 3) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "dev-runner/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status < 500
    except Exception:
        return False


# ── Container runtime detection ───────────────────────────────────────────────

def container_runtime() -> str:
    """Return 'podman' if available, else 'docker', else ''."""
    for rt in ("podman", "docker"):
        if shutil.which(rt):
            return rt
    return ""


# ── Service start / stop ──────────────────────────────────────────────────────

_pids: dict[str, int] = {}


def _start_venv_service(svc: ServiceConfig) -> Optional[int]:
    """Start a Python/Node service in the background, redirect to log file."""
    if not svc.cwd.exists():
        err(f"{svc.name}: directory not found — {svc.cwd}")
        return None

    log_path = svc.log_file
    env = {**os.environ, **svc.env_extra}

    with open(log_path, "a") as logf:
        proc = subprocess.Popen(
            svc.start_cmd,
            cwd=svc.cwd,
            env=env,
            stdout=logf,
            stderr=logf,
            start_new_session=True,
        )
    ok(f"{svc.name} started  PID={proc.pid}  log={log_path}")
    return proc.pid


def _start_container(svc: ServiceConfig) -> bool:
    """Start expert backend via Podman or Docker compose."""
    rt = container_runtime()
    if not rt:
        err("No container runtime found (podman / docker). Cannot start Expert backend.")
        return False

    if not svc.cwd.exists():
        err(f"Expert backend directory not found — {svc.cwd}")
        return False

    # Try compose first, fall back to plain run
    compose_file = svc.cwd / "docker-compose.yml"
    if compose_file.exists():
        cmd = [rt, "compose", "up", "-d", "expert-backend"]
    else:
        warn(f"No docker-compose.yml found in {svc.cwd} — trying podman run")
        cmd = [
            rt, "run", "-d",
            "--name", svc.container_name,
            "--env-file", str(svc.cwd / ".env"),
            "-p", f"{svc.port}:{svc.port}",
            "-v", f"{svc.cwd}:/app",
            "integral-expert-backend:latest",
        ]

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=svc.cwd)
    if result.returncode == 0:
        ok(f"{svc.name} container started via {rt}")
        return True
    else:
        err(f"{svc.name} container failed: {result.stderr.strip()}")
        return False


def start_service(svc: ServiceConfig) -> bool:
    step(f"Starting {svc.name} backend on :{svc.port}")

    if svc.use_container:
        return _start_container(svc)

    pid = _start_venv_service(svc)
    if pid:
        _pids[svc.name] = pid
        return True
    return False


def stop_all() -> None:
    step("Stopping all services…")

    # Kill venv processes
    for port in [8000, 8003, 5173]:
        subprocess.run(
            f"lsof -ti:{port} | xargs kill -TERM 2>/dev/null || true",
            shell=True
        )

    # Stop container
    rt = container_runtime()
    if rt:
        cwd = ROOT / "integral-expert-backend"
        compose_file = cwd / "docker-compose.yml"
        if compose_file.exists():
            subprocess.run([rt, "compose", "down"], cwd=cwd, capture_output=True)
        else:
            subprocess.run([rt, "stop", "integral-expert-backend"], capture_output=True)

    ok("All services stopped.")


# ── Health check ──────────────────────────────────────────────────────────────

def run_health_check() -> bool:
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"  🩺 Integral Market Health Check — {ts()} UTC")
    print(f"{BOLD}{'='*60}{RESET}\n")

    all_ok = True

    # Infrastructure
    pg_ok = check_postgres()
    if pg_ok:
        ok(f"PostgreSQL  :5432  accepting connections")
    else:
        err(f"PostgreSQL  :5432  NOT READY — run: sudo systemctl start postgresql")
        all_ok = False

    try:
        redis_ok = check_redis()
    except Exception:
        redis_ok = False
    if redis_ok:
        ok(f"Redis       :6380  PONG")
    else:
        err(f"Redis       :6380  NOT READY — run: sudo systemctl start redis")
        all_ok = False

    print()

    # Services
    for svc in SERVICES:
        up = check_http(svc.health_url)
        label = f"{svc.name:<10} :{svc.port}"
        if up:
            ok(f"{label}  healthy")
        else:
            err(f"{label}  DOWN — check {svc.log_file}")
            all_ok = False

    print()
    if all_ok:
        print(f"{GREEN}{BOLD}🎉  All services healthy.{RESET}\n")
    else:
        print(f"{RED}{BOLD}⛔  One or more services are down. Check logs above.{RESET}\n")

    return all_ok


# ── Log streaming ─────────────────────────────────────────────────────────────

LOG_LABELS = {
    "/tmp/market-backend.log": (BLUE,    "[MARKET]"),
    "/tmp/imi-backend.log":    (YELLOW,  "[IMI]  "),
    "/tmp/frontend.log":       (CYAN,    "[FRONT]"),
    "/tmp/expert-backend.log": (MAGENTA, "[EXPERT]"),
}


def follow_logs() -> None:
    """Tail all log files simultaneously using a subprocess."""
    log_files = [svc.log_file for svc in SERVICES]
    existing = [f for f in log_files if Path(f).exists()]

    if not existing:
        warn("No log files found yet — start services first")
        return

    info(f"Streaming logs: {', '.join(existing)}")
    info("Press Ctrl+C to stop.\n")

    try:
        proc = subprocess.Popen(
            ["tail", "-f"] + existing,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        current_file = ""
        for line in proc.stdout:  # type: ignore[union-attr]
            # tail -f emits "==> filename <==" headers when following multiple files
            if line.startswith("==>") and "<==" in line:
                current_file = line.strip().split("==>")[1].split("<==")[0].strip()
                continue
            color, label = LOG_LABELS.get(current_file, (WHITE, "[LOG]  "))
            print(f"{color}{ts()} {label}{RESET} {line}", end="")
    except KeyboardInterrupt:
        print("\nLog streaming stopped.")
        if proc:
            proc.terminate()


# ── Watch mode ────────────────────────────────────────────────────────────────

def watch_mode(follow: bool) -> None:
    """Check service health every 10s; restart failed services."""
    info("Watch mode active — auto-restarting failed services.")
    info("Press Ctrl+C to stop.\n")

    try:
        while True:
            for svc in SERVICES:
                if not check_http(svc.health_url, timeout=2):
                    warn(f"{svc.name} is down — attempting restart…")
                    start_service(svc)
                    time.sleep(3)
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nWatch mode stopped.")


# ── Wait for service ──────────────────────────────────────────────────────────

def wait_for(svc: ServiceConfig, timeout: int = 30) -> bool:
    """Poll until service responds or timeout."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if check_http(svc.health_url, timeout=2):
            return True
        time.sleep(2)
    return False


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Integral Market full-stack dev runner.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--start-all", action="store_true", help="Start all services")
    parser.add_argument("--stop-all",  action="store_true", help="Stop all services")
    parser.add_argument("--health",    action="store_true", help="Health check all services")
    parser.add_argument("--logs",      action="store_true", help="Stream existing logs")
    parser.add_argument("--follow",    action="store_true", help="Stream logs after starting")
    parser.add_argument("--watch",     action="store_true", help="Auto-restart failed services")
    parser.add_argument("--service",   help="Target a single service (market|expert|imi|frontend)")

    args = parser.parse_args()

    if args.stop_all:
        stop_all()
        return

    if args.health:
        healthy = run_health_check()
        sys.exit(0 if healthy else 1)

    if args.logs:
        follow_logs()
        return

    if args.start_all:
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"  🚀 Integral Market Dev Runner — {ts()} UTC")
        print(f"{BOLD}{'='*60}{RESET}\n")

        # Infrastructure check
        step("Checking infrastructure…")
        if not check_postgres():
            err("PostgreSQL is not running. Start it first:")
            print("  sudo systemctl start postgresql")
            print("  OR: podman run -d --name postgres -p 5432:5432 timescale/timescaledb:latest-pg15")
            sys.exit(1)
        ok("PostgreSQL :5432")

        try:
            redis_ok = check_redis()
        except Exception:
            redis_ok = False
        if not redis_ok:
            warn("Redis :6380 not responding — some features may fail")
        else:
            ok("Redis :6380")

        print()

        # Filter to single service if requested
        targets = SERVICES
        if args.service:
            targets = [s for s in SERVICES if s.name.lower() == args.service.lower()]
            if not targets:
                err(f"Unknown service: {args.service}. Valid: market, expert, imi, frontend")
                sys.exit(1)

        # Start services in order
        for svc in targets:
            start_service(svc)
            time.sleep(1)   # brief stagger to avoid port race

        # Wait for backends before starting frontend
        print()
        step("Waiting for backends to become healthy…")
        for svc in targets:
            if svc.name in ("Market", "Expert", "IMI"):
                up = wait_for(svc, timeout=30)
                if up:
                    ok(f"{svc.name} healthy at :{svc.port}")
                else:
                    warn(f"{svc.name} did not respond in 30s — check {svc.log_file}")

        print()
        run_health_check()

        if args.follow or args.watch:
            print()
            if args.watch:
                watch_mode(follow=args.follow)
            else:
                follow_logs()

        return

    # Default: just print help
    parser.print_help()


if __name__ == "__main__":
    main()
