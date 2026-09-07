#!/usr/bin/env python3
"""
MCP Runner
Utility to start a specified MCP server in a subprocess and handle basic lifecycle.
Usage:
    python3 mcp_runner.py <server_name>
where <server_name> is one of: memory_server, token_optimization_server, architecture_mcp_server
The runner will locate the corresponding script in the same directory and execute it.
It forwards stdin/stdout to allow JSON-RPC communication.
"""
import subprocess
import sys
import pathlib

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 mcp_runner.py <server_name>")
        sys.exit(1)
    server = sys.argv[1]
    allowed = {
        "memory_server": "memory_server.py",
        "token_optimization_server": "token_optimization_server.py",
        "architecture_mcp_server": "architecture_mcp_server.py",
    }
    if server not in allowed:
        print(f"Unknown server '{server}'. Allowed: {', '.join(allowed)}")
        sys.exit(1)
    script_path = pathlib.Path(__file__).with_name(allowed[server])
    if not script_path.exists():
        print(f"Server script not found: {script_path}")
        sys.exit(1)
    # Run the server as a subprocess, inheriting stdio for JSON-RPC
    proc = subprocess.Popen([sys.executable, str(script_path)], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    main()
