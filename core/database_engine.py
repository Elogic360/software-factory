"""
Software Factory Database Engineering Plane.
Provides schema discovery, ERD generation (Mermaid & Draw.io),
migration safety verification, and schema-to-model drift detection.
"""

import json
import re
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

class DatabaseEngine:
    """Database schema discovery, ERD diagram generation, and migration safety checker."""

    def __init__(self, evidence_dir: Optional[str] = None):
        if evidence_dir is None:
            self.evidence_dir = Path(__file__).resolve().parent.parent / "evidence" / "database"
        else:
            self.evidence_dir = Path(evidence_dir)
        self.evidence_dir.mkdir(parents=True, exist_ok=True)

    def parse_sql_ddl(self, ddl_text: str) -> Dict[str, Any]:
        """Parses standard SQL DDL (CREATE TABLE, ALTER TABLE, CREATE INDEX) into a schema representation."""
        schema: Dict[str, Any] = {"tables": {}, "indexes": []}

        # Match CREATE TABLE statements
        table_pattern = re.compile(
            r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?["`]?([a-zA-Z0-9_]+)["`]?\s*\((.*?)\);',
            re.IGNORECASE | re.DOTALL
        )

        for match in table_pattern.finditer(ddl_text):
            table_name = match.group(1)
            body = match.group(2)

            columns = {}
            primary_keys = []
            foreign_keys = []

            # Split columns by comma outside parenthesis
            lines = [line.strip() for line in body.split("\n") if line.strip()]
            for line in lines:
                line = line.rstrip(",")
                if not line:
                    continue

                u_line = line.upper()
                if u_line.startswith("PRIMARY KEY"):
                    pk_match = re.search(r'\((.*?)\)', line)
                    if pk_match:
                        primary_keys.extend([col.strip(' "`') for col in pk_match.group(1).split(",")])
                elif u_line.startswith("FOREIGN KEY"):
                    fk_match = re.search(r'FOREIGN\s+KEY\s*\((.*?)\)\s*REFERENCES\s+["`]?([a-zA-Z0-9_]+)["`]?\s*\((.*?)\)', line, re.IGNORECASE)
                    if fk_match:
                        foreign_keys.append({
                            "column": fk_match.group(1).strip(' "`'),
                            "ref_table": fk_match.group(2).strip(' "`'),
                            "ref_column": fk_match.group(3).strip(' "`')
                        })
                elif u_line.startswith("CONSTRAINT") and "FOREIGN KEY" in u_line:
                    fk_match = re.search(r'FOREIGN\s+KEY\s*\((.*?)\)\s*REFERENCES\s+["`]?([a-zA-Z0-9_]+)["`]?\s*\((.*?)\)', line, re.IGNORECASE)
                    if fk_match:
                        foreign_keys.append({
                            "column": fk_match.group(1).strip(' "`'),
                            "ref_table": fk_match.group(2).strip(' "`'),
                            "ref_column": fk_match.group(3).strip(' "`')
                        })
                else:
                    parts = line.split()
                    if len(parts) >= 2:
                        col_name = parts[0].strip(' "`')
                        col_type = parts[1].upper()
                        is_pk = "PRIMARY KEY" in u_line
                        is_nullable = "NOT NULL" not in u_line
                        if is_pk and col_name not in primary_keys:
                            primary_keys.append(col_name)
                        columns[col_name] = {
                            "type": col_type,
                            "nullable": is_nullable,
                            "is_primary_key": is_pk
                        }

            schema["tables"][table_name] = {
                "columns": columns,
                "primary_keys": primary_keys,
                "foreign_keys": foreign_keys
            }

        # Match CREATE INDEX statements
        index_pattern = re.compile(
            r'CREATE\s+(UNIQUE\s+)?INDEX\s+(?:IF\s+NOT\s+EXISTS\s+)?["`]?([a-zA-Z0-9_]+)["`]?\s+ON\s+["`]?([a-zA-Z0-9_]+)["`]?\s*\((.*?)\);',
            re.IGNORECASE
        )
        for match in index_pattern.finditer(ddl_text):
            schema["indexes"].append({
                "name": match.group(2),
                "is_unique": bool(match.group(1)),
                "table": match.group(3),
                "columns": [c.strip(' "`') for c in match.group(4).split(",")]
            })

        return schema

    def generate_mermaid_erd(self, schema: Dict[str, Any]) -> str:
        """Generates Mermaid erDiagram markdown from schema representation."""
        lines = ["erDiagram"]
        tables = schema.get("tables", {})

        for table_name, t_data in tables.items():
            lines.append(f"    {table_name} {{")
            for col_name, c_data in t_data.get("columns", {}).items():
                c_type = c_data.get("type", "string").lower().replace("(", "_").replace(")", "")
                pk_marker = "PK" if col_name in t_data.get("primary_keys", []) else ""
                lines.append(f"        {c_type} {col_name} {pk_marker}".strip())
            lines.append("    }")

        # Render relationships
        for table_name, t_data in tables.items():
            for fk in t_data.get("foreign_keys", []):
                ref_table = fk.get("ref_table")
                if ref_table in tables:
                    lines.append(f'    {ref_table} ||--o{{ {table_name} : "{fk.get("column")} -> {fk.get("ref_column")}"')

        return "\n".join(lines)

    def generate_drawio_xml(self, schema: Dict[str, Any]) -> str:
        """Generates a structured Draw.io XML representation of the database schema."""
        cells = [
            '<mxGraphModel dx="1000" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169">',
            '  <root>',
            '    <mxCell id="0"/>',
            '    <mxCell id="1" parent="0"/>'
        ]

        x = 40
        y = 40
        cell_id = 2

        for table_name, t_data in schema.get("tables", {}).items():
            cols = t_data.get("columns", {})
            height = 30 + (len(cols) * 20)
            col_list = "<br/>".join([f"{c}: {d.get('type')}" for c, d in cols.items()])
            label = f"&lt;b&gt;{table_name}&lt;/b&gt;&lt;hr/&gt;{col_list}"

            cells.append(
                f'    <mxCell id="{cell_id}" value="{label}" style="shape=table;whiteSpace=wrap;html=1;fillColor=#1e293b;strokeColor=#475569;fontColor=#f8fafc;" vertex="1" parent="1">'
            )
            cells.append(
                f'      <mxGeometry x="{x}" y="{y}" width="220" height="{height}" as="geometry"/>'
            )
            cells.append('    </mxCell>')

            cell_id += 1
            x += 260
            if x > 800:
                x = 40
                y += 240

        cells.append('  </root>')
        cells.append('</mxGraphModel>')
        return "\n".join(cells)

    def verify_migration_safety(self, migration_sql: str) -> Dict[str, Any]:
        """Inspects SQL migration for dangerous or breaking operations."""
        warnings = []
        hazards = []

        m_upper = migration_sql.upper()

        # Destructive table drops
        if "DROP TABLE" in m_upper:
            hazards.append({
                "rule": "DESTRUCTIVE_DROP_TABLE",
                "severity": "CRITICAL",
                "description": "Migration contains DROP TABLE which permanently destroys data."
            })

        # Destructive column drops
        if "DROP COLUMN" in m_upper:
            hazards.append({
                "rule": "DESTRUCTIVE_DROP_COLUMN",
                "severity": "HIGH",
                "description": "Migration drops a column without backward-compatible transition phase."
            })

        # NOT NULL without DEFAULT
        if "ADD COLUMN" in m_upper and "NOT NULL" in m_upper and "DEFAULT" not in m_upper:
            hazards.append({
                "rule": "NON_NULL_WITHOUT_DEFAULT",
                "severity": "HIGH",
                "description": "Adding a NOT NULL column without DEFAULT will fail on tables with existing rows."
            })

        # Renaming tables/columns directly
        if "RENAME TO" in m_upper or "RENAME COLUMN" in m_upper:
            warnings.append({
                "rule": "BREAKING_RENAME",
                "severity": "MEDIUM",
                "description": "Direct renaming breaks running application queries during rolling deployments."
            })

        # Full table locks
        if "LOCK TABLE" in m_upper:
            warnings.append({
                "rule": "TABLE_LOCK",
                "severity": "MEDIUM",
                "description": "Explicit table locking will cause connection queuing and latency spikes."
            })

        is_safe = len(hazards) == 0
        report = {
            "safe": is_safe,
            "status": "APPROVED" if is_safe else "REJECTED",
            "hazards_count": len(hazards),
            "warnings_count": len(warnings),
            "hazards": hazards,
            "warnings": warnings,
            "timestamp": time.time()
        }

        artifact_path = self.evidence_dir / f"migration_safety_{int(time.time()*1000)}.json"
        with open(artifact_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        report["evidence_file"] = str(artifact_path)
        return report

    def detect_schema_drift(self, expected_models: Dict[str, Any], live_schema: Dict[str, Any]) -> Dict[str, Any]:
        """Compares expected code models against actual database schema to detect drift."""
        missing_tables = []
        extra_tables = []
        column_mismatches = []

        expected_tables = expected_models.get("tables", {})
        live_tables = live_schema.get("tables", {})

        for t in expected_tables:
            if t not in live_tables:
                missing_tables.append(t)
            else:
                exp_cols = expected_tables[t].get("columns", {})
                live_cols = live_tables[t].get("columns", {})
                for c, exp_meta in exp_cols.items():
                    if c not in live_cols:
                        column_mismatches.append(f"Table '{t}': missing column '{c}'.")
                    else:
                        live_meta = live_cols[c]
                        if exp_meta.get("type") and live_meta.get("type"):
                            if exp_meta["type"].upper() != live_meta["type"].upper():
                                column_mismatches.append(
                                    f"Table '{t}', Column '{c}': type mismatch (expected {exp_meta['type']}, got {live_meta['type']})."
                                )

        for t in live_tables:
            if t not in expected_tables:
                extra_tables.append(t)

        drift_found = bool(missing_tables or column_mismatches)
        report = {
            "drift_detected": drift_found,
            "missing_tables": missing_tables,
            "extra_tables": extra_tables,
            "column_mismatches": column_mismatches,
            "status": "DRIFT_DETECTED" if drift_found else "IN_SYNC",
            "timestamp": time.time()
        }

        artifact_path = self.evidence_dir / f"schema_drift_{int(time.time()*1000)}.json"
        with open(artifact_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        report["evidence_file"] = str(artifact_path)
        return report
