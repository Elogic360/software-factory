"""
Software Factory — Spec Kit Adapter & Specification-Driven Development Engine.
Integrates github/spec-kit and dceoy/speckit-agent-skills with TargetEngine and ArchitectureState.
Provides requirement interrogation (/grill-with-docs pattern) and spec-to-target compilation.
"""

import re
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml

from core.target_engine import TargetEngine


class SpecKitAdapter:
    """Bridges Spec-Driven Development (SDD) into actionable factory manufacturing targets."""

    def __init__(self, workspace_root: Optional[str] = None):
        if workspace_root is None:
            self.workspace_root = Path(__file__).resolve().parent.parent
        else:
            self.workspace_root = Path(workspace_root)

    def parse_markdown_sections(self, content: str) -> Dict[str, str]:
        """Parses Markdown content into dictionary of header sections."""
        sections: Dict[str, str] = {}
        current_header = 'preamble'
        current_lines: List[str] = []

        for line in content.splitlines():
            header_match = re.match(r'^(#{1,3})\s+(.+)$', line)
            if header_match:
                if current_lines:
                    sections[current_header.strip().lower()] = "\n".join(current_lines).strip()
                    current_lines = []
                current_header = header_match.group(2)
            else:
                current_lines.append(line)

        if current_lines:
            sections[current_header.strip().lower()] = "\n".join(current_lines).strip()

        return sections

    def parse_tasks(self, tasks_md: str) -> List[Dict[str, Any]]:
        """Parses tasks.md into structured task objects."""
        tasks: List[Dict[str, Any]] = []
        current_task: Optional[Dict[str, Any]] = None

        lines = tasks_md.splitlines()
        for line in lines:
            task_match = re.match(r'^[-*]\s+\[([ xX])\]\s+([A-Za-z0-9_.-]+(?:\s*:\s*|\s+))?(.+)$', line)
            if not task_match:
                header_match = re.match(r'^#{2,4}\s+(Task\s+[\w.-]+:?\s*)(.+)$', line, re.IGNORECASE)
                if header_match:
                    task_id = header_match.group(1).strip().replace(':', '').replace(' ', '-').upper()
                    title = header_match.group(2).strip()
                    current_task = {
                        'task_id': task_id,
                        'title': title,
                        'completed': False,
                        'criteria': [],
                        'category': 'general'
                    }
                    tasks.append(current_task)
                    continue
            else:
                is_done = task_match.group(1).lower() == 'x'
                raw_id = (task_match.group(2) or '').strip().rstrip(':')
                title = task_match.group(3).strip()
                task_id = raw_id if raw_id else f'TASK-{len(tasks) + 1:03d}'

                category = 'general'
                lower_title = title.lower()
                if any(w in lower_title for w in ['db', 'schema', 'table', 'migration', 'sql', 'postgres']):
                    category = 'database'
                elif any(w in lower_title for w in ['api', 'endpoint', 'rest', 'router', 'route']):
                    category = 'api'
                elif any(w in lower_title for w in ['ui', 'frontend', 'view', 'component', 'screen', 'css']):
                    category = 'ui'
                elif any(w in lower_title for w in ['auth', 'security', 'jwt', 'rbac', 'token']):
                    category = 'security'

                current_task = {
                    'task_id': task_id,
                    'title': title,
                    'completed': is_done,
                    'criteria': [],
                    'category': category
                }
                tasks.append(current_task)
                continue

            if current_task and re.match(r'^\s+[-*]\s+(.+)$', line):
                crit = re.match(r'^\s+[-*]\s+(.+)$', line).group(1).strip()
                current_task['criteria'].append(crit)

        return tasks

    def compile_spec_to_targets(
        self,
        spec_content: str,
        tasks_content: str,
        target_engine: Optional[TargetEngine] = None
    ) -> List[Dict[str, Any]]:
        """Compiles spec.md and tasks.md into factory TargetEngine target records."""
        parsed_tasks = self.parse_tasks(tasks_content)
        spec_sections = self.parse_markdown_sections(spec_content)

        created_targets: List[Dict[str, Any]] = []
        engine = target_engine or TargetEngine()

        for idx, task in enumerate(parsed_tasks):
            t_id = f'TGT-{task["task_id"]}' if not task['task_id'].startswith('TGT-') else task['task_id']
            t_id = re.sub(r'[^A-Za-z0-9_-]', '-', t_id).upper()

            criteria = task['criteria']
            if not criteria:
                criteria = [f'Complete implementation of {task["title"]}', 'Pass test verification']

            existing = engine.get_target(t_id)
            if existing:
                created_targets.append(existing)
                continue

            target = engine.create_target(
                target_id=t_id,
                title=task['title'],
                description=f'Generated from Spec Kit task {task["task_id"]}: {task["title"]}',
                category=task['category'],
                acceptance_criteria=criteria,
                owner='SpecKitAdapter'
            )
            created_targets.append(target)

        return created_targets

    def compile_spec_to_c4_architecture(self, spec_content: str, plan_content: str) -> Dict[str, Any]:
        """Compiles spec & plan into C4 architecture model (Context, Container, Component)."""
        sections = self.parse_markdown_sections(spec_content)
        h1_match = re.search(r"^#\s+(.+)$", spec_content, re.MULTILINE)
        if h1_match:
            system_name = h1_match.group(1).strip()
        else:
            system_name = 'TargetSystem'

        containers = [
            {
                'name': 'WebFrontend',
                'type': 'Web Application',
                'technology': 'React / TypeScript / Tailwind',
                'description': 'User interface for operations and interactions.'
            },
            {
                'name': 'ApiGateway',
                'type': 'API Service',
                'technology': 'FastAPI / Python',
                'description': 'REST endpoints and business logic.'
            },
            {
                'name': 'PrimaryDatabase',
                'type': 'Relational Database',
                'technology': 'PostgreSQL 16',
                'description': 'Persistent data storage with strict RBAC.'
            }
        ]

        components = [
            {'name': 'AuthService', 'container': 'ApiGateway', 'responsibility': 'JWT issuance, RBAC, session check'},
            {'name': 'ResourceService', 'container': 'ApiGateway', 'responsibility': 'CRUD lifecycle operations'},
            {'name': 'AuditLogger', 'container': 'ApiGateway', 'responsibility': 'Immutable audit events'}
        ]

        return {
            'version': '1.0',
            'system_name': system_name,
            'c4_levels': {
                'context': {
                    'primary_actor': 'End User / Operator',
                    'system': system_name,
                    'external_systems': ['Authentication Provider', 'Notification Service']
                },
                'containers': containers,
                'components': components,
                'invariants': [
                    'No client direct write to PrimaryDatabase',
                    'All APIs authenticated via Bearer token',
                    'All schema changes applied via versioned migrations'
                ]
            },
            'generated_at': time.time()
        }

    def interrogate_requirements(self, spec_content: str) -> Dict[str, Any]:
        """Runs requirement interrogation (/grill-with-docs pattern) to uncover edge cases and ambiguities."""
        clarifications = []

        if not re.search(r'(auth|jwt|rbac|permission|role|session|login)', spec_content, re.IGNORECASE):
            clarifications.append({
                'area': 'Security & Authentication',
                'question': 'What is the authorization model? (Who can create, read, update, delete resources?)',
                'severity': 'HIGH',
                'recommendation': 'Specify RBAC roles (e.g. Admin, Member, Guest) and token expiration policies.'
            })

        if not re.search(r'(error|exception|failure|retry|rollback|status code)', spec_content, re.IGNORECASE):
            clarifications.append({
                'area': 'Resilience & Error Handling',
                'question': 'How should failures be handled? What are the standard error response schemas and HTTP codes?',
                'severity': 'HIGH',
                'recommendation': 'Define structured JSON error schema: {error: {code, message, details}}.'
            })

        if not re.search(r'(latency|qps|rps|throughput|p95|concurrency|sla)', spec_content, re.IGNORECASE):
            clarifications.append({
                'area': 'Performance & SLAs',
                'question': 'What are the performance baselines? (p95 latency threshold, concurrent users, request volume)?',
                'severity': 'MEDIUM',
                'recommendation': 'Default baseline: p95 latency < 150ms, support >= 100 concurrent requests.'
            })

        if not re.search(r'(database|postgres|schema|table|migration|persistence)', spec_content, re.IGNORECASE):
            clarifications.append({
                'area': 'Data Persistence',
                'question': 'Where is the state stored, and what is the database schema definition?',
                'severity': 'HIGH',
                'recommendation': 'Provide DDL schema with foreign keys, indexes, and migration rollback scripts.'
            })

        if not re.search(r'(metrics|logs|tracing|healthcheck|prometheus|sentry)', spec_content, re.IGNORECASE):
            clarifications.append({
                'area': 'Observability',
                'question': 'How will health and telemetry be monitored in production?',
                'severity': 'MEDIUM',
                'recommendation': 'Define /health and /metrics endpoints plus structured JSON logging.'
            })

        readiness_score = max(0, 100 - (len(clarifications) * 15))

        return {
            'status': 'APPROVED' if readiness_score >= 80 else 'NEEDS_CLARIFICATION',
            'readiness_score': readiness_score,
            'total_questions': len(clarifications),
            'clarifications': clarifications
        }
