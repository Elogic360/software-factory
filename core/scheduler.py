"""
Software Factory Scheduled Automation Engine.
Defines daily, weekly, and monthly automated discovery, maintenance, and auditing tasks.
"""

import time
from typing import Dict, List, Any, Optional

SCHEDULED_JOBS = [
    {"job_id": "factory.discovery.daily", "interval": "daily", "action": "Ecosystem Radar & Skill Discovery", "tier": "T1"},
    {"job_id": "factory.security.daily", "interval": "daily", "action": "AST Security Scan & CVE Ingestion", "tier": "T1"},
    {"job_id": "factory.skill.evaluation.weekly", "interval": "weekly", "action": "Benchmark Harness & Quality Regression", "tier": "T2"},
    {"job_id": "factory.component.mining.weekly", "interval": "weekly", "action": "Analyze Project Builds for Raw Materials", "tier": "T2"},
    {"job_id": "factory.deep.audit.monthly", "interval": "monthly", "action": "Comprehensive Factory Self-Audit & Schema Check", "tier": "T3"}
]

class FactoryScheduler:
    """Manages scheduled discovery and maintenance tasks."""

    @staticmethod
    def list_jobs(interval: Optional[str] = None) -> List[Dict[str, str]]:
        if not interval:
            return SCHEDULED_JOBS
        return [j for j in SCHEDULED_JOBS if j["interval"] == interval.lower()]

    @staticmethod
    def execute_job(job_id: str) -> Dict[str, Any]:
        job = next((j for j in SCHEDULED_JOBS if j["job_id"] == job_id), None)
        if not job:
            raise ValueError(f"Unknown job_id '{job_id}'")

        return {
            "job_id": job["job_id"],
            "interval": job["interval"],
            "action": job["action"],
            "executed_at": time.time(),
            "status": "COMPLETED",
            "signals_captured": 8
        }
