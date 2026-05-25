#!/usr/bin/env python3
"""
skill_selector.py — Agentic Skill Router for Integral Market Software-Factory

Given a task description, ranks and returns the most relevant SKILL.md files
so an agent can load exactly the right institutional knowledge for the job.

Usage:
    python3 skill_selector.py --query "add WebSocket live positions to imCharts"
    python3 skill_selector.py --query "optimize slow journal analytics query" --top 3
    python3 skill_selector.py --query "backtest RSI strategy" --load   # prints full skill content
    python3 skill_selector.py --list                                    # list all skills
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ── Skill definitions ─────────────────────────────────────────────────────────
# Each skill has: directory name, display name, and activation trigger phrases.
# Triggers are matched against the user's query (case-insensitive, partial).
# Add new skills here when adding to skills/.

SKILLS: list[dict] = [
    {
        "dir": "skill-builder",
        "name": "Skill Builder (Meta)",
        "layer": "Meta",
        "triggers": [
            "create new skill", "add skill", "skill template", "skill quality",
            "knowledge codification", "agent knowledge base", "extend software-factory",
            "skill audit", "new engineering domain", "skill review",
        ],
    },
    {
        "dir": "software-product-architect",
        "name": "Software Product Architect",
        "layer": "Product",
        "triggers": [
            "prd", "product requirements", "user story", "acceptance criteria",
            "feature scope", "roadmap", "mvp", "feature prioritization", "rice score",
            "persona", "stakeholder", "out of scope", "success metric",
        ],
    },
    {
        "dir": "architect-principal",
        "name": "Principal Architect",
        "layer": "Architecture",
        "triggers": [
            "architecture decision", "adr", "service design", "system design",
            "service boundary", "scalability", "schema ownership", "dependency analysis",
            "technical trade-off", "monolith", "service decomposition", "design pattern",
        ],
    },
    {
        "dir": "software-developer",
        "name": "Software Developer",
        "layer": "General",
        "triggers": [
            "code review", "refactoring", "debugging", "code quality", "naming convention",
            "code smell", "technical debt", "guard clause", "extract function",
            "git workflow", "commit message", "dead code", "god function",
        ],
    },
    {
        "dir": "backend-fastapi",
        "name": "Backend (FastAPI)",
        "layer": "Backend",
        "triggers": [
            "fastapi endpoint", "sqlalchemy model", "pydantic schema", "async route",
            "dependency injection", "exception handler", "global handler", "middleware",
            "orm relationship", "registry collision", "selectinload", "mapped_column",
            "alembic", "router", "depends", "httpexception",
        ],
    },
    {
        "dir": "database-postgresql",
        "name": "Database (PostgreSQL)",
        "layer": "Database",
        "triggers": [
            "migration", "schema design", "timescaledb", "hypertable", "continuous aggregate",
            "rbac function", "is_admin", "index", "foreignkey", "multi-schema",
            "data migration", "pg_dump", "alembic", "postgresql", "postgres",
        ],
    },
    {
        "dir": "frontend-react",
        "name": "Frontend (React)",
        "layer": "Frontend",
        "triggers": [
            "react component", "typescript type", "zustand store", "react query",
            "usequery", "usemutation", "tanstack query", "custom hook", "lazy loading",
            "code splitting", "module structure", "barrel export", "tsx", "vite",
        ],
    },
    {
        "dir": "frontend-trading-ui",
        "name": "Frontend Trading UI",
        "layer": "Frontend",
        "triggers": [
            "trading interface", "chart panel", "watchlist", "journal entry",
            "copy trading ui", "provider card", "trade history table", "pnl display",
            "broker account connection panel", "positions table", "order panel",
            "signal feed", "imcharts", "imjournal", "imcopying",
        ],
    },
    {
        "dir": "ui-ux-premium",
        "name": "UI/UX Premium Design",
        "layer": "Design",
        "triggers": [
            "page design", "component styling", "design token", "glassmorphism",
            "dark mode", "responsive layout", "animation", "accessibility",
            "color system", "glasscard", "gradient border", "tailwind", "framer motion",
            "wcag", "aria",
        ],
    },
    {
        "dir": "security-audit",
        "name": "Security Audit",
        "layer": "Security",
        "triggers": [
            "jwt access token", "refresh token rotation", "bcrypt", "account lockout",
            "oauth", "cors configuration", "rate limiting", "sql injection",
            "security headers", "credential storage", "fernet encryption", "rbac",
            "permission check", "authentication", "authorization",
        ],
    },
    {
        "dir": "devops-engineer",
        "name": "DevOps Engineer",
        "layer": "Infra",
        "triggers": [
            "dockerfile", "docker-compose", "ci pipeline", "deployment",
            "environment config", "service startup", "health check", "scaling",
            "github actions", "env var", "dev-start", "ci/cd", "container",
        ],
    },
    {
        "dir": "observability",
        "name": "Observability",
        "layer": "Infra",
        "triggers": [
            "structured logging", "metrics endpoint", "prometheus", "grafana",
            "opentelemetry", "distributed tracing", "json logs", "alert rule",
            "loki", "health dashboard", "performance monitoring", "span", "trace",
        ],
    },
    {
        "dir": "performance-engineering",
        "name": "Performance Engineering",
        "layer": "Performance",
        "triggers": [
            "slow query", "n+1", "n+1 problem", "cache strategy", "pagination",
            "response time", "database index", "redis cache", "query explain",
            "profiling", "lazy loading", "connection pool", "selectinload",
            "cursor pagination", "offset", "bottleneck", "optimize",
        ],
    },
    {
        "dir": "seo-optimizer",
        "name": "SEO Optimizer",
        "layer": "Frontend",
        "triggers": [
            "meta tags", "open graph", "sitemap", "robots.txt", "structured data",
            "page title", "canonical url", "core web vitals", "ssr", "landing page seo",
            "search ranking", "social sharing", "seohead", "noindex",
        ],
    },
    {
        "dir": "mt5-integration",
        "name": "MT5 Integration",
        "layer": "Trading",
        "triggers": [
            "mt5 connection", "trade sync", "broker adapter", "execution gateway",
            "position management", "order placement", "brokerregistry", "mt5 windows bridge",
            "sync worker", "apscheduler", "fernet encrypted credentials", "broker",
        ],
    },
    {
        "dir": "copytrading-engine",
        "name": "Copy Trading Engine",
        "layer": "Trading",
        "triggers": [
            "copy trading", "provider registration", "subscription", "signal routing",
            "risk limits", "performance tracking", "execution log", "copysubscription",
            "providersignal", "copy_ratio", "drawdown check", "lot size", "provider",
            "subscriber", "copy mode", "mirror",
        ],
    },
    {
        "dir": "journal-analytics",
        "name": "Journal Analytics",
        "layer": "Trading",
        "triggers": [
            "trading journal", "trade analytics", "performance metrics", "win rate",
            "profit factor", "sharpe ratio", "drawdown calculation", "equity curve",
            "calendar heatmap", "trade annotation", "journal entry",
            "timescaledb continuous aggregate", "daily stats",
        ],
    },
    {
        "dir": "tradingview-integration",
        "name": "TradingView Integration",
        "layer": "Trading",
        "triggers": [
            "tradingview chart", "custom data feed", "ohlcv bars", "chart widget",
            "symbol search", "order markers", "lightweight charts", "charting configuration",
            "candlestick", "equity curve chart", "bar", "volume",
        ],
    },
    {
        "dir": "websocket-realtime",
        "name": "WebSocket & Realtime",
        "layer": "Realtime",
        "triggers": [
            "websocket endpoint", "live price feed", "real-time positions",
            "signal streaming", "notification push", "pub/sub channel", "redis streams",
            "connection management", "reconnection logic", "connectionmanager",
            "useexpertws", "ws", "live", "realtime", "real-time",
        ],
    },
    {
        "dir": "redis-streams",
        "name": "Redis Streams",
        "layer": "Infra",
        "triggers": [
            "redis streams", "consumer groups", "rate limiting", "session cache",
            "redis pub/sub", "message queue", "job queue", "leaky bucket",
            "token bucket", "redis data structures", "xadd", "xreadgroup", "xack",
            "sliding window",
        ],
    },
    {
        "dir": "event-driven-architecture",
        "name": "Event-Driven Architecture",
        "layer": "Architecture",
        "triggers": [
            "domain event", "event bus", "pub/sub architecture", "cqrs", "saga pattern",
            "event sourcing", "async workflow", "decoupled service", "domainevent",
            "fan-out", "at-least-once delivery", "event driven",
        ],
    },
    {
        "dir": "microservices",
        "name": "Microservices",
        "layer": "Architecture",
        "triggers": [
            "new service", "service boundary", "inter-service call", "api gateway",
            "kong", "service discovery", "microservice design", "service contract",
            "service decomposition", "internal api", "serviceclient",
        ],
    },
    {
        "dir": "prompt-engineering",
        "name": "Prompt Engineering",
        "layer": "AI",
        "triggers": [
            "llm integration", "ai feature", "prompt template", "agent design",
            "context window", "few-shot examples", "chain-of-thought", "structured output",
            "function calling", "market intelligence ai", "tool use", "system prompt",
            "anthropic", "claude",
        ],
    },
    {
        "dir": "ai-optimization",
        "name": "AI Optimization",
        "layer": "AI",
        "triggers": [
            "ai pipeline", "llm inference cost", "model selection", "caching ai responses",
            "streaming", "batching", "quality evaluation", "a/b testing prompts",
            "ai feature scaling", "claude-haiku", "claude-opus", "claude-sonnet",
            "sse stream", "token cost",
        ],
    },
    {
        "dir": "context-engineering",
        "name": "Context Engineering",
        "layer": "AI",
        "triggers": [
            "context window", "token budget", "agent memory", "information retrieval",
            "context snapshot", "session compression", "rag", "semantic search",
            "long conversation", "context overflow", "snapshot.py", "retriever.py",
        ],
    },
    {
        "dir": "quant-research",
        "name": "Quantitative Research",
        "layer": "Quant",
        "triggers": [
            "trading strategy", "backtest", "alpha signal", "statistical analysis",
            "risk-adjusted return", "monte carlo", "walk-forward analysis",
            "strategy optimization", "quant model", "sharpe ratio", "profit factor",
            "drawdown simulation",
        ],
    },
    {
        "dir": "testing-e2e",
        "name": "Testing (E2E + Integration)",
        "layer": "Testing",
        "triggers": [
            "test writing", "api test", "end-to-end test", "playwright", "pytest",
            "test fixture", "mock", "factory pattern", "coverage report",
            "ci test pipeline", "pytest-asyncio", "asyncclient", "factory_boy",
            "integration test", "unit test",
        ],
    },
    {
        "dir": "testing-load",
        "name": "Load Testing",
        "layer": "Testing",
        "triggers": [
            "load test", "performance benchmark", "concurrent users", "throughput",
            "locust", "k6", "capacity planning", "stress test", "spike test",
            "bottleneck", "latency under load", "sla validation", "p99",
        ],
    },
    {
        "dir": "change-detective",
        "name": "Change Detective",
        "layer": "DevProcess",
        "triggers": [
            "change detection", "detect changes", "what changed", "diff analysis",
            "auto-document", "schema drift", "api drift", "type drift",
            "undocumented change", "changelog", "audit trail", "memory update",
            "codebase drift", "breaking change", "regression risk", "change_detector",
        ],
    },
    {
        "dir": "interactive-dev",
        "name": "Interactive Development",
        "layer": "DevProcess",
        "triggers": [
            "interactive dev", "live debugging", "full-stack debug", "run all services",
            "capture logs", "browser logs", "backend logs", "postgres logs",
            "reproduce bug", "end-to-end debug", "dev runner", "watch mode",
            "hot reload", "inspect network", "inspect error", "dev session",
            "stack trace", "frontend error", "backend error", "500 error",
            "cors debug", "websocket debug", "ui bug",
        ],
    },
    {
        "dir": "software-product-tester",
        "name": "Software & Product Tester",
        "layer": "Testing",
        "triggers": [
            "product testing", "software testing", "qa", "test plan", "regression test",
            "bug report", "bug reproduction", "acceptance test", "uat", "ui test",
            "browser test", "api test", "integration test", "smoke test",
            "accessibility", "a11y", "wcag", "cross-browser", "visual regression",
            "test coverage", "test suite", "playwright", "verify this works",
        ],
    },
    {
        "dir": "mt5-scalability",
        "name": "MT5 Scalability Architecture",
        "layer": "Trading",
        "triggers": [
            "mt5 scalability", "metatrader5 scale", "10000 users", "concurrent mt5",
            "broker connection pool", "mt5 worker", "mt5 queue", "mt5 sync",
            "mt5 bridge", "trading account sync", "copy trading scale",
            "broker gateway scale", "mt5 connection limit", "mt5 horizontal scaling",
            "redis queue mt5", "websocket mt5", "position sync", "order sync",
            "mt5 circuit breaker", "10k users",
        ],
    },
]


# ── Scoring engine ─────────────────────────────────────────────────────────────

@dataclass
class SkillMatch:
    skill: dict
    score: int
    matched_triggers: list[str] = field(default_factory=list)

    @property
    def stars(self) -> str:
        max_score = 5
        filled = min(self.score, max_score)
        return "★" * filled + "☆" * (max_score - filled)

    @property
    def skill_path(self) -> Path:
        sf_root = Path(__file__).parent.parent
        return sf_root / "skills" / self.skill["dir"] / "SKILL.md"


def score_skills(query: str, skills: list[dict]) -> list[SkillMatch]:
    """Score each skill against the query and return sorted matches."""
    query_lower = query.lower()
    query_words = set(re.findall(r"\b\w{3,}\b", query_lower))
    matches = []

    for skill in skills:
        score = 0
        matched = []

        for trigger in skill["triggers"]:
            trigger_lower = trigger.lower()
            trigger_words = set(re.findall(r"\b\w{3,}\b", trigger_lower))

            # Exact phrase match (highest weight)
            if trigger_lower in query_lower:
                score += 3
                matched.append(trigger)
            # Word overlap (partial match)
            elif overlap := trigger_words & query_words:
                score += len(overlap)
                matched.append(f"~{trigger}")

        if score > 0:
            matches.append(SkillMatch(skill=skill, score=score, matched_triggers=matched))

    matches.sort(key=lambda m: m.score, reverse=True)
    return matches


# ── CLI ────────────────────────────────────────────────────────────────────────

def cmd_query(query: str, top: int, load: bool, verbose: bool) -> None:
    matches = score_skills(query, SKILLS)

    if not matches:
        print("No skills matched. Try broader terms or use --list.")
        sys.exit(0)

    top_matches = matches[:top]
    print(f"\n🎯 Skill matches for: \"{query}\"\n")

    for i, m in enumerate(top_matches):
        path_exists = "✅" if m.skill_path.exists() else "⚠️  (file missing)"
        print(f"  {i+1}. {m.stars}  [{m.skill['layer']}] {m.skill['name']}")
        print(f"      Path:  skills/{m.skill['dir']}/SKILL.md {path_exists}")
        if verbose:
            print(f"      Score: {m.score}  Matched: {', '.join(m.matched_triggers[:4])}")
        print()

    # Print ready-to-use shell command
    print("─" * 60)
    print("Load into agent session:")
    for m in top_matches:
        print(f"  cat software-factory/skills/{m.skill['dir']}/SKILL.md")

    if load:
        print("\n" + "=" * 70)
        for m in top_matches:
            if m.skill_path.exists():
                print(f"\n{'='*70}")
                print(f"# SKILL: {m.skill['name']}")
                print(f"{'='*70}\n")
                print(m.skill_path.read_text())
            else:
                print(f"\n⚠️  {m.skill_path} not found")


def cmd_list() -> None:
    print("\n📚 All registered skills:\n")
    by_layer: dict[str, list] = {}
    for skill in SKILLS:
        by_layer.setdefault(skill["layer"], []).append(skill)

    for layer, skills_in_layer in sorted(by_layer.items()):
        print(f"  {layer}:")
        for skill in skills_in_layer:
            sf_root = Path(__file__).parent.parent
            skill_path = sf_root / "skills" / skill["dir"] / "SKILL.md"
            status = "✅" if skill_path.exists() else "❌"
            print(f"    {status} {skill['dir']:<35} {skill['name']}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Select the right SKILL.md for your task.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 skill_selector.py --query "add WebSocket live positions to imCharts"
  python3 skill_selector.py --query "optimize slow journal analytics query" --top 3
  python3 skill_selector.py --query "backtest RSI strategy" --load
  python3 skill_selector.py --list
        """,
    )
    parser.add_argument("--query", "-q", help="Task description to match skills against")
    parser.add_argument("--top", "-n", type=int, default=3, help="Number of top matches to return (default: 3)")
    parser.add_argument("--load", "-l", action="store_true", help="Print full skill content after matches")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show match scores and trigger details")
    parser.add_argument("--list", action="store_true", help="List all registered skills")

    args = parser.parse_args()

    if args.list:
        cmd_list()
    elif args.query:
        cmd_query(args.query, args.top, args.load, args.verbose)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
