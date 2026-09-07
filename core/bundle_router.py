"""
Software Factory Capability Bundles & Intelligent Tool Router.
Packages capabilities into 12 coherent task-based bundles and routes agent queries
to the minimal, highest-leverage toolset to maximize accuracy and conserve tokens.
"""

from typing import Dict, List, Any, Optional

CAPABILITY_BUNDLES: Dict[str, Dict[str, Any]] = {
    "browser-engineering": {
        "id": "browser-engineering",
        "name": "Browser Engineering & Visual QA",
        "description": "Headless browser automation, visual inspection, accessibility (axe-core), and responsive viewport validation.",
        "skills": ["browser-qa", "accessibility", "e2e-testing", "ui-demo"],
        "tools": ["playwright-cli", "chrome-devtools-mcp", "playwright-mcp", "browser-use"],
        "keywords": ["browser", "ui", "dom", "click", "viewport", "accessibility", "a11y", "axe", "screenshot", "e2e", "visual"]
    },
    "api-engineering": {
        "id": "api-engineering",
        "name": "API Engineering & Contract Testing",
        "description": "OpenAPI 3.x schema validation, contract-first test generation, and runtime API drift detection.",
        "skills": ["api-design", "im-api-contracts", "api-connector-builder"],
        "tools": ["api_testing_engine", "curl", "postman_mcp", "openapi_generator"],
        "keywords": ["api", "rest", "endpoint", "contract", "openapi", "swagger", "http", "route", "payload", "json"]
    },
    "database-engineering": {
        "id": "database-engineering",
        "name": "Database Engineering & Architecture",
        "description": "Schema discovery, ERD diagram generation (Mermaid/Draw.io), migration safety analysis, and schema drift detection.",
        "skills": ["database-postgresql", "database-migrations", "postgres-patterns", "im-postgres", "im-timescaledb"],
        "tools": ["database_engine", "psql", "alembic", "prisma"],
        "keywords": ["database", "sql", "postgres", "table", "schema", "erd", "migration", "indexes", "query", "drift"]
    },
    "frontend-engineering": {
        "id": "frontend-engineering",
        "name": "Frontend Engineering & Design System",
        "description": "Modern frontend patterns, component composition, state management, and design system integration.",
        "skills": ["frontend-patterns", "frontend-trading-ui", "design-system", "motion-patterns", "im-react"],
        "tools": ["npm", "vite", "tailwind", "eslint"],
        "keywords": ["frontend", "react", "vue", "tailwind", "css", "component", "state", "animation", "motion", "ui"]
    },
    "backend-engineering": {
        "id": "backend-engineering",
        "name": "Backend Engineering & Service Architecture",
        "description": "High-performance backend service patterns, dependency injection, and transactional service design.",
        "skills": ["fastapi-patterns", "backend-patterns", "im-fastapi", "golang-patterns", "springboot-patterns"],
        "tools": ["pytest", "fastapi", "uvicorn", "docker"],
        "keywords": ["backend", "fastapi", "service", "handler", "controller", "transaction", "auth", "middleware"]
    },
    "security-engineering": {
        "id": "security-engineering",
        "name": "Security Engineering & Supply Chain",
        "description": "Static analysis, agent supply-chain security, OWASP top 10 verification, and secret detection.",
        "skills": ["security-review", "security-audit", "security-scan", "im-security", "llm-trading-agent-security"],
        "tools": ["ecc-agentshield", "semgrep", "trufflehog", "bandit"],
        "keywords": ["security", "vulnerability", "token", "cve", "auth", "jwt", "secret", "owasp", "injection"]
    },
    "observability-sre": {
        "id": "observability-sre",
        "name": "Observability & SRE",
        "description": "Structured telemetry, OpenTelemetry, metrics visualization, and system health monitoring.",
        "skills": ["im-observability", "dashboard-builder", "testing-load"],
        "tools": ["sentry", "prometheus", "grafana", "signoz"],
        "keywords": ["observability", "sre", "metrics", "tracing", "telemetry", "latency", "health", "dashboard", "alert"]
    },
    "performance-engineering": {
        "id": "performance-engineering",
        "name": "Performance Engineering & Profiling",
        "description": "Performance profiling, query optimization, Core Web Vitals, and latency acceleration.",
        "skills": ["performance-engineering", "latency-critical-systems", "data-throughput-accelerator", "benchmark"],
        "tools": ["lighthouse", "cprofile", "py-spy", "memray"],
        "keywords": ["performance", "speed", "latency", "benchmark", "optimize", "slow", "profiler", "throughput"]
    },
    "architecture-governance": {
        "id": "architecture-governance",
        "name": "Architecture Governance & Invariants",
        "description": "Section 22 architecture state compilation, boundary validation, and architectural invariant checks.",
        "skills": ["im-architecture", "architect-principal", "hexagonal-architecture", "drawio-diagrams"],
        "tools": ["architecture_state", "spec_compiler", "codegraph"],
        "keywords": ["architecture", "boundaries", "invariants", "adr", "c4", "module", "system", "design", "specification"]
    },
    "target-verification": {
        "id": "target-verification",
        "name": "Target-Driven Development (TDD) & Gates",
        "description": "Goal-oriented Target state machine enforcement, verification gates, and evidence collection.",
        "skills": ["tdd-workflow", "eval-harness", "verification-loop", "im-release-gate"],
        "tools": ["target_engine", "pytest", "gate_checker"],
        "keywords": ["target", "tdd", "goal", "verification", "gates", "acceptance", "evidence", "progress", "milestone"]
    },
    "cross-layer-debugging": {
        "id": "cross-layer-debugging",
        "name": "Cross-Layer Debugging & RCA",
        "description": "Full-stack log correlation across UI, Network, API, Backend, and Database to deduce root causes.",
        "skills": ["agent-introspection-debugging", "change-detective", "terminal-ops"],
        "tools": ["cross_layer_debugger", "browser_orchestrator", "log_correlator"],
        "keywords": ["debug", "error", "trace", "correlation", "incident", "failure", "crash", "rca", "cross-layer"]
    },
    "autonomous-manufacturing": {
        "id": "autonomous-manufacturing",
        "name": "Autonomous Software Manufacturing",
        "description": "End-to-end spec compilation, automated BOM generation, work order execution, and production release gates.",
        "skills": ["autonomous-loops", "ralphinho-rfc-pipeline", "im-software-factory", "continuous-agent-loop"],
        "tools": ["manufacturing_line", "bom_generator", "agent_control_plane"],
        "keywords": ["manufacturing", "factory", "assembly", "work order", "bom", "spec", "autonomous", "release"]
    }
}

class BundleRouter:
    """Intelligent router for capability bundles and minimal toolsets."""

    def __init__(self):
        self.bundles = CAPABILITY_BUNDLES

    def get_bundle(self, bundle_id: str) -> Optional[Dict[str, Any]]:
        """Returns details of a capability bundle."""
        return self.bundles.get(bundle_id)

    def list_bundles(self) -> List[Dict[str, Any]]:
        """Returns all 12 registered capability bundles."""
        return list(self.bundles.values())

    def route_query(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        """Matches a user or agent prompt to the best-fit capability bundles."""
        q_lower = query.lower()
        q_tokens = set(q_lower.replace("-", " ").replace("_", " ").split())

        scored = []
        for b_id, bundle in self.bundles.items():
            score = 0
            # Check keywords
            for kw in bundle["keywords"]:
                if kw in q_lower:
                    score += 3
            # Check bundle id and name
            if b_id in q_lower or bundle["name"].lower() in q_lower:
                score += 5
            # Token overlap in description
            desc_tokens = set(bundle["description"].lower().split())
            score += len(q_tokens.intersection(desc_tokens))

            scored.append({"bundle": bundle, "score": score})

        scored.sort(key=lambda x: x["score"], reverse=True)
        top_matches = [item["bundle"] for item in scored[:top_k] if item["score"] > 0]
        if not top_matches:
            # Fallback to general autonomous-manufacturing and architecture-governance
            top_matches = [self.bundles["autonomous-manufacturing"], self.bundles["architecture-governance"]]

        return top_matches
