"""
core/interfaces.py — Canonical Modular Interfaces for Software Factory OS
Defines pluggable abstract base classes for discovery, security, memory,
benchmarking, agent adapters, sandboxing, and evidence capture.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path

class CapabilityProvider(ABC):
    @abstractmethod
    def list_capabilities(self) -> List[Dict[str, Any]]: ...
    @abstractmethod
    def get_capability(self, capability_id: str) -> Optional[Dict[str, Any]]: ...

class SkillProvider(ABC):
    @abstractmethod
    def discover_skills(self, source_path: Path) -> List[Dict[str, Any]]: ...
    @abstractmethod
    def route_skills(self, query: str, context: Dict[str, Any]) -> List[Dict[str, Any]]: ...

class MCPProvider(ABC):
    @abstractmethod
    def list_servers(self) -> List[Dict[str, Any]]: ...
    @abstractmethod
    def verify_server(self, server_name: str) -> Tuple[bool, str]: ...

class SecurityScanner(ABC):
    @abstractmethod
    def scan_code(self, target_path: Path) -> Dict[str, Any]: ...
    @abstractmethod
    def scan_skill(self, skill_file: Path) -> Dict[str, Any]: ...

class LicenseScanner(ABC):
    @abstractmethod
    def evaluate_license(self, license_str: str) -> str: ...

class MemoryProvider(ABC):
    @abstractmethod
    def recall_decisions(self, query: str) -> List[Dict[str, Any]]: ...
    @abstractmethod
    def record_decision(self, title: str, content: str, author: str) -> bool: ...

class BenchmarkProvider(ABC):
    @abstractmethod
    def run_benchmark(self, task_name: str, config: Dict[str, Any]) -> Dict[str, Any]: ...

class EvidenceProvider(ABC):
    @abstractmethod
    def record_evidence(self, task_id: str, artifact_type: str, data: Any) -> str: ...
    @abstractmethod
    def verify_evidence(self, evidence_id: str) -> bool: ...

class AgentAdapter(ABC):
    @abstractmethod
    def configure_workspace(self, target_dir: Path, sf_dir: Path) -> bool: ...
