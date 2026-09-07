"""
core/mcp_runner.py — Real MCP Process Supervisor for the Software Factory.

Replaces the dummy `echo 'ok'` healthcheck in factory.py with actual
JSON-RPC 2.0 stdio handshakes. Provides start/stop/restart/health_check
per server, credential injection from env vars, and permission tier gating.

Usage:
    from pathlib import Path
    from core.mcp_runner import MCPRunner
    runner = MCPRunner(sf_root=Path('.'))
    print(runner.health_check('factory-memory-mcp'))
    print(runner.list_all())
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
    _YAML_OK = True
except ImportError:
    _YAML_OK = False

HEALTHCHECK_TIMEOUT_SECS = 8
SHUTDOWN_GRACE_SECS = 3
WRITE_TIERS = {"T3", "T4"}


class MCPRunner:
    """Central MCP process supervisor for the Software Factory."""

    def __init__(self, sf_root: Path):
        self.sf_root = Path(sf_root).resolve()
        self._registry_path = self.sf_root / "registries" / "mcp_registry.yaml"
        self._processes: Dict[str, subprocess.Popen] = {}

    def _load_registry(self) -> List[Dict[str, Any]]:
        if not self._registry_path.exists() or not _YAML_OK:
            return []
        with open(self._registry_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data.get("mcp_servers", [])

    def _get_server_def(self, server_id: str) -> Optional[Dict[str, Any]]:
        for srv in self._load_registry():
            if srv.get("id") == server_id:
                return srv
        return None

    def _build_env(self, server_def: Dict[str, Any]) -> Dict[str, str]:
        env = dict(os.environ)
        for key, value in (server_def.get("env") or {}).items():
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                var_name = value[2:-1]
                resolved = os.environ.get(var_name, "")
                if not resolved:
                    sys.stderr.write(
                        f"[MCPRunner] WARNING: {server_def['id']} needs {var_name} but it is not set.\n"
                    )
                env[key] = resolved
            else:
                env[key] = str(value)
        return env

    def _resolve_command(self, server_def: Dict[str, Any]) -> List[str]:
        cmd = server_def.get("command", "")
        args = list(server_def.get("args") or [])
        if cmd in ("python3", "python") and args:
            first = args[0]
            if first.startswith("./") or (first.endswith(".py") and not first.startswith("/")):
                args = [str(self.sf_root / first)] + args[1:]
        return [cmd] + [str(a) for a in args]

    def _check_permission(self, server_def: Dict[str, Any], allow_write: bool = False) -> None:
        tier = server_def.get("permission_tier", "T1")
        if tier in WRITE_TIERS and not allow_write:
            raise PermissionError(
                f"Server '{server_def['id']}' has permission_tier={tier} "
                "(write-capable). Pass allow_write=True to start it explicitly."
            )

    def start(self, server_id: str, allow_write: bool = False) -> Dict[str, Any]:
        srv = self._get_server_def(server_id)
        if not srv:
            return {"server_id": server_id, "status": "ERROR", "error": "Not found in registry"}
        if srv.get("evaluation_status") == "BLOCKED":
            return {"server_id": server_id, "status": "BLOCKED", "error": "Blocked by policy"}
        try:
            self._check_permission(srv, allow_write=allow_write)
        except PermissionError as e:
            return {"server_id": server_id, "status": "PERMISSION_DENIED", "error": str(e)}
        if server_id in self._processes and self._processes[server_id].poll() is None:
            return {"server_id": server_id, "status": "ALREADY_RUNNING", "pid": self._processes[server_id].pid}
        cmd = self._resolve_command(srv)
        env = self._build_env(srv)
        try:
            proc = subprocess.Popen(
                cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True, env=env, cwd=str(self.sf_root)
            )
            self._processes[server_id] = proc
            return {"server_id": server_id, "status": "STARTED", "pid": proc.pid}
        except FileNotFoundError as e:
            return {"server_id": server_id, "status": "ERROR", "error": f"Command not found: {e}"}
        except Exception as e:
            return {"server_id": server_id, "status": "ERROR", "error": str(e)}

    def stop(self, server_id: str) -> Dict[str, Any]:
        if server_id not in self._processes:
            return {"server_id": server_id, "status": "NOT_RUNNING"}
        proc = self._processes[server_id]
        if proc.poll() is not None:
            del self._processes[server_id]
            return {"server_id": server_id, "status": "ALREADY_STOPPED"}
        proc.terminate()
        try:
            proc.wait(timeout=SHUTDOWN_GRACE_SECS)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
        del self._processes[server_id]
        return {"server_id": server_id, "status": "STOPPED"}

    def restart(self, server_id: str, allow_write: bool = False) -> Dict[str, Any]:
        self.stop(server_id)
        return self.start(server_id, allow_write=allow_write)

    def health_check(self, server_id: str) -> Dict[str, Any]:
        """Real JSON-RPC 2.0 healthcheck: launch → initialize → verify serverInfo → terminate."""
        srv = self._get_server_def(server_id)
        if not srv:
            return {"server_id": server_id, "status": "UNKNOWN", "error": "Not found in mcp_registry.yaml"}
        if srv.get("evaluation_status") == "BLOCKED":
            return {"server_id": server_id, "status": "BLOCKED", "error": "Blocked by policy"}
        if srv.get("evaluation_status") == "CANDIDATE":
            return {"server_id": server_id, "status": "CANDIDATE", "error": "Awaiting evaluation pipeline"}

        cmd = self._resolve_command(srv)
        env = self._build_env(srv)
        proc = None
        try:
            proc = subprocess.Popen(
                cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True, env=env, cwd=str(self.sf_root)
            )
            init_req = json.dumps({
                "jsonrpc": "2.0", "id": 1, "method": "initialize",
                "params": {"protocolVersion": "2024-11-05",
                           "clientInfo": {"name": "mcp-runner-healthcheck", "version": "1.0"},
                           "capabilities": {}}
            }) + "\n"
            try:
                proc.stdin.write(init_req)
                proc.stdin.flush()
            except BrokenPipeError:
                stderr_out = proc.stderr.read(500) if proc.stderr else ""
                return {"server_id": server_id, "status": "FAILED",
                        "error": f"Server exited immediately. stderr: {stderr_out}"}

            response_lines: List[str] = []
            stderr_lines: List[str] = []

            def _read_stdout():
                try:
                    line = proc.stdout.readline()
                    if line:
                        response_lines.append(line.strip())
                except Exception:
                    pass

            def _read_stderr():
                try:
                    line = proc.stderr.readline()
                    if line:
                        stderr_lines.append(line.strip())
                except Exception:
                    pass

            t1 = threading.Thread(target=_read_stdout, daemon=True)
            t2 = threading.Thread(target=_read_stderr, daemon=True)
            t1.start(); t2.start()
            t1.join(timeout=HEALTHCHECK_TIMEOUT_SECS)
            t2.join(timeout=0.5)

            if not response_lines:
                stderr_info = " | ".join(stderr_lines[:3]) if stderr_lines else "no stderr"
                return {"server_id": server_id, "status": "FAILED",
                        "error": f"No response within {HEALTHCHECK_TIMEOUT_SECS}s. stderr: {stderr_info}"}

            try:
                response = json.loads(response_lines[0])
            except json.JSONDecodeError:
                return {"server_id": server_id, "status": "FAILED",
                        "error": f"Non-JSON response: {response_lines[0][:200]}"}

            if "error" in response:
                return {"server_id": server_id, "status": "FAILED",
                        "error": f"JSON-RPC error: {response['error']}"}

            server_info = response.get("result", {}).get("serverInfo", {})
            if not server_info:
                return {"server_id": server_id, "status": "DEGRADED",
                        "error": "initialize responded but serverInfo missing"}

            return {
                "server_id": server_id, "status": "HEALTHY",
                "server_name": server_info.get("name"),
                "server_version": server_info.get("version"),
                "trust_level": srv.get("evaluation_status", "UNKNOWN"),
                "permission_tier": srv.get("permission_tier", "T1"),
            }
        except FileNotFoundError:
            return {"server_id": server_id, "status": "FAILED",
                    "error": f"Command not found: {srv.get('command')} — not installed"}
        except Exception as e:
            return {"server_id": server_id, "status": "ERROR", "error": str(e)}
        finally:
            if proc and proc.poll() is None:
                try:
                    proc.terminate(); proc.wait(timeout=2)
                except Exception:
                    try: proc.kill()
                    except Exception: pass

    def list_all(self) -> List[Dict[str, Any]]:
        results = []
        for srv in self._load_registry():
            proc = self._processes.get(srv["id"])
            running = proc is not None and proc.poll() is None
            results.append({
                "server_id": srv.get("id"), "name": srv.get("name"),
                "evaluation_status": srv.get("evaluation_status", "UNKNOWN"),
                "permission_tier": srv.get("permission_tier", "T1"),
                "transport": srv.get("transport", "stdio"),
                "running": running, "pid": proc.pid if running else None,
            })
        return results

    def health_check_all(self, skip_candidates: bool = True) -> List[Dict[str, Any]]:
        results = []
        for srv in self._load_registry():
            status = srv.get("evaluation_status", "UNKNOWN")
            if skip_candidates and status in ("CANDIDATE", "BLOCKED"):
                results.append({"server_id": srv["id"], "status": status, "skipped": True})
                continue
            results.append(self.health_check(srv["id"]))
        return results

    def start_all(self, allow_write: bool = False) -> List[Dict[str, Any]]:
        return [self.start(srv["id"], allow_write=allow_write)
                for srv in self._load_registry()
                if srv.get("evaluation_status") in ("PRODUCTION_APPROVED", "VERIFIED")]

    def stop_all(self) -> List[Dict[str, Any]]:
        return [self.stop(sid) for sid in list(self._processes.keys())]
