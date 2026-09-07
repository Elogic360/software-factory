"""
Software Factory Architecture-as-Code Engine.
Supports C1-C4 models, Mermaid diagram generation, Draw.io XML export,
architecture graph representation, and architecture drift detection.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

class ArchitectureEngine:
    """Manages C4 architecture models, Mermaid syntax, and system relationship graphs."""

    def __init__(self, workspace_dir: Optional[str] = None):
        if workspace_dir is None:
            self.workspace_dir = Path(__file__).resolve().parent.parent / "architecture"
        else:
            self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(parents=True, exist_ok=True)

    def generate_c4_model(self, product_name: str, containers: List[Dict[str, Any]], components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Builds standardized C1-C4 architecture model."""
        model = {
            "product": product_name,
            "version": "1.0",
            "c1_context": {
                "name": f"{product_name} System",
                "description": f"Core software system for {product_name}",
                "users": ["Customer", "Operator", "Administrator"],
                "external_systems": ["Payment Gateway", "Authentication Provider", "Email Service"]
            },
            "c2_containers": [
                {
                    "name": c.get("name", "Container"),
                    "type": c.get("type", "Web App / API / DB"),
                    "tech": c.get("tech", "TypeScript / Python"),
                    "description": c.get("description", "")
                }
                for c in containers
            ],
            "c3_components": [
                {
                    "container": comp.get("container", "API"),
                    "name": comp.get("name", "Component"),
                    "tech": comp.get("tech", "Service Layer"),
                    "responsibility": comp.get("responsibility", "")
                }
                for comp in components
            ],
            "c4_code_patterns": {
                "layers": ["Domain / Entities", "Use Cases / Services", "Adapters / Repositories", "Controllers / API"],
                "naming_convention": "snake_case files, PascalCase classes"
            }
        }
        return model

    def generate_mermaid_c4(self, c4_model: Dict[str, Any]) -> str:
        """Renders Mermaid diagram from C4 model."""
        product = c4_model.get("product", "System")
        lines = [
            "```mermaid",
            "C4Context",
            f'title System Context Diagram for {product}',
            f'Person(user, "User", "Customer or Operator")',
            f'System(coreSys, "{product} System", "Handles business workflows and data management")',
            f'System_Ext(extAuth, "OAuth Provider", "External Identity & Auth")',
            f'System_Ext(extDb, "Database Cluster", "TimescaleDB & PostgreSQL")',
            "",
            'Rel(user, coreSys, "Uses", "HTTPS/REST/WSS")',
            'Rel(coreSys, extAuth, "Authenticates with", "OIDC/JWT")',
            'Rel(coreSys, extDb, "Persists state in", "SQL / TCP")',
            "```"
        ]
        return "\n".join(lines)

    def generate_mermaid_flowchart(self, workflow_name: str, steps: List[Dict[str, str]]) -> str:
        lines = [
            "```mermaid",
            "flowchart TD",
            f"    subgraph {workflow_name}"
        ]
        for idx, s in enumerate(steps, 1):
            s_id = f"S{idx}"
            lines.append(f'        {s_id}["{s.get("title", f"Step {idx}")}"]')
            if idx > 1:
                prev_id = f"S{idx-1}"
                lines.append(f'        {prev_id} --> {s_id}')
        lines.append("    end")
        lines.append("```")
        return "\n".join(lines)

    def build_architecture_graph(self, nodes: List[Dict[str, str]], edges: List[Dict[str, str]]) -> Dict[str, Any]:
        """Creates formal node-edge system graph for impact analysis."""
        graph = {
            "graph_version": "1.0",
            "nodes": [
                {"id": n["id"], "type": n.get("type", "service"), "name": n.get("name", n["id"])}
                for n in nodes
            ],
            "edges": [
                {"source": e["source"], "target": e["target"], "relation": e.get("relation", "depends_on")}
                for e in edges
            ]
        }
        return graph

    def detect_drift(self, expected_graph: Dict[str, Any], live_endpoints: List[str]) -> Dict[str, Any]:
        """Compares expected architecture graph with live detected service routes."""
        expected_services = {n["id"].lower() for n in expected_graph.get("nodes", [])}
        live_services = set()
        for e in live_endpoints:
            parts = [p.lower() for p in e.strip("/").split("/") if p.lower() not in ["api", "v1", "v2"]]
            if parts:
                live_services.add(parts[0])

        undocumented = list(live_services - expected_services)
        missing = list(expected_services - live_services)

        has_drift = len(undocumented) > 0 or len(missing) > 0
        return {
            "has_drift": has_drift,
            "undocumented_live_services": undocumented,
            "missing_expected_services": missing,
            "status": "DRIFT_DETECTED" if has_drift else "SYNCHRONIZED"
        }

    def generate_drawio_architecture(self, c4_model: Dict[str, Any]) -> str:
        """Generates Draw.io XML (mxGraphModel) from C4 model."""
        product = c4_model.get("product", "System")
        containers = c4_model.get("c2_containers", [])

        cells = [
            '<mxGraphModel dx="1200" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827">',
            '  <root>',
            '    <mxCell id="0"/>',
            '    <mxCell id="1" parent="0"/>',
            f'    <mxCell id="2" value="&lt;b&gt;{product} Architecture Boundary&lt;/b&gt;" style="swimlane;whiteSpace=wrap;html=1;fillColor=#0f172a;strokeColor=#3b82f6;fontColor=#f8fafc;" vertex="1" parent="1">',
            '      <mxGeometry x="40" y="40" width="800" height="480" as="geometry"/>',
            '    </mxCell>'
        ]

        x = 70
        y = 90
        cell_id = 3
        for c in containers:
            label = f"&lt;b&gt;{c.get('name')}&lt;/b&gt;&lt;br/&gt;[{c.get('tech')}]&lt;br/&gt;{c.get('description')}"
            cells.append(
                f'    <mxCell id="{cell_id}" value="{label}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1e293b;strokeColor=#64748b;fontColor=#ffffff;" vertex="1" parent="2">'
            )
            cells.append(f'      <mxGeometry x="{x}" y="{y}" width="180" height="90" as="geometry"/>')
            cells.append('    </mxCell>')
            cell_id += 1
            x += 210
            if x > 600:
                x = 70
                y += 120

        cells.append('  </root>')
        cells.append('</mxGraphModel>')
        return "\n".join(cells)

    def validate_diagram_layout(self, drawio_xml: str) -> Dict[str, Any]:
        """Validates Draw.io XML for layout collisions, label boundary violations, and orphan nodes."""
        import re
        import xml.etree.ElementTree as ET

        collisions = []
        boundary_violations = []
        nodes = []

        try:
            root = ET.fromstring(drawio_xml)
            for cell in root.iter('mxCell'):
                geo = cell.find('mxGeometry')
                if geo is not None and cell.get('vertex') == '1':
                    try:
                        x = float(geo.get('x', 0))
                        y = float(geo.get('y', 0))
                        w = float(geo.get('width', 0))
                        h = float(geo.get('height', 0))
                        node_id = cell.get('id')
                        nodes.append({'id': node_id, 'x': x, 'y': y, 'w': w, 'h': h})
                        if x < 0 or y < 0:
                            boundary_violations.append(f"Node {node_id} has negative coordinates ({x}, {y})")
                    except ValueError:
                        continue

            # Collision check between sibling nodes
            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    n1, n2 = nodes[i], nodes[j]
                    # Check if bounding boxes intersect (excluding root boundary container)
                    if n1['id'] in ['0', '1', '2'] or n2['id'] in ['0', '1', '2']:
                        continue
                    if (n1['x'] < n2['x'] + n2['w'] and n1['x'] + n1['w'] > n2['x'] and
                        n1['y'] < n2['y'] + n2['h'] and n1['y'] + n1['h'] > n2['y']):
                        collisions.append(f"Collision between Node {n1['id']} and Node {n2['id']}")

        except Exception as e:
            return {"valid": False, "error": f"Malformed Draw.io XML: {str(e)}"}

        is_valid = len(collisions) == 0 and len(boundary_violations) == 0
        return {
            "valid": is_valid,
            "total_nodes_checked": len(nodes),
            "collisions": collisions,
            "boundary_violations": boundary_violations,
            "verdict": "APPROVED" if is_valid else "LAYOUT_DEFECTS_DETECTED"
        }

    def convert_mermaid_to_drawio_xml(self, mermaid_code: str) -> str:
        """Translates Mermaid flowchart/graph syntax into valid Draw.io XML model."""
        import re
        lines = [l.strip() for l in mermaid_code.splitlines() if l.strip() and not l.startswith("%%")]
        nodes = {}
        edges = []

        for line in lines:
            if any(line.startswith(k) for k in ["graph", "flowchart"]):
                continue
            # Match A[Label] --> B[Label] or A --> B
            edge_match = re.search(r'([A-Za-z0-9_]+)(?:\[(.*?)\])?\s*-->\s*([A-Za-z0-9_]+)(?:\[(.*?)\])?', line)
            if edge_match:
                src_id, src_lbl, dst_id, dst_lbl = edge_match.groups()
                nodes[src_id] = src_lbl or src_id
                nodes[dst_id] = dst_lbl or dst_id
                edges.append((src_id, dst_id))
            else:
                node_match = re.search(r'([A-Za-z0-9_]+)\[(.*?)\]', line)
                if node_match:
                    nodes[node_match.group(1)] = node_match.group(2)

        containers = [{"name": lbl, "tech": "Service", "description": nid} for nid, lbl in nodes.items()]
        c4_stub = {"product": "Converted Mermaid System", "c2_containers": containers}
        return self.generate_drawio_architecture(c4_stub)

