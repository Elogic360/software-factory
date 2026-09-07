"""
DEPRECATED — Forwards to the canonical mcp/memory_server.py.
Use factory-memory-mcp (mcp/memory_server.py) directly.
This shim maintains backward compatibility.
"""
import subprocess, sys
from pathlib import Path
canonical = Path(__file__).parent.parent / "mcp" / "memory_server.py"
proc = subprocess.Popen([sys.executable, str(canonical)], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
try:
    proc.wait()
except KeyboardInterrupt:
    proc.terminate()
    proc.wait()
