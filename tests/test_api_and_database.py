import pytest
from core.api_testing_engine import APITestingEngine
from core.database_engine import DatabaseEngine

def test_api_spec_validation_and_generation():
    engine = APITestingEngine()
    valid_spec = {
        "openapi": "3.0.3",
        "info": {"title": "Market API", "version": "1.0.0"},
        "paths": {
            "/api/v1/orders": {
                "get": {
                    "operationId": "get_orders",
                    "responses": {"200": {"description": "List orders"}}
                },
                "post": {
                    "operationId": "create_order",
                    "responses": {
                        "201": {
                            "description": "Order created",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "order_id": {"type": "string"},
                                            "amount": {"type": "integer"}
                                        },
                                        "required": ["order_id", "amount"]
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    val = engine.validate_spec_structure(valid_spec)
    assert val["valid"] is True
    assert val["total_paths"] == 1

    suite = engine.generate_contract_test_suite(valid_spec)
    assert len(suite) == 2
    post_test = [t for t in suite if t["method"] == "POST"][0]
    assert post_test["expected_status"] == 201

def test_api_contract_verification_pass_and_fail():
    engine = APITestingEngine()
    spec = {
        "openapi": "3.0.3",
        "info": {"title": "Test API", "version": "1.0.0"},
        "paths": {
            "/api/v1/users/{id}": {
                "get": {
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "string"},
                                            "age": {"type": "integer"}
                                        },
                                        "required": ["id", "age"]
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    # Successful call
    res_pass = engine.verify_response_against_contract("/api/v1/users/123", "GET", 200, {"id": "u-123", "age": 30}, spec)
    assert res_pass["verdict"] == "PASSED"

    # Missing required field
    res_fail_missing = engine.verify_response_against_contract("/api/v1/users/123", "GET", 200, {"id": "u-123"}, spec)
    assert res_fail_missing["verdict"] == "FAILED"
    assert any("age" in m for m in res_fail_missing["schema_mismatches"])

    # Wrong type
    res_fail_type = engine.verify_response_against_contract("/api/v1/users/123", "GET", 200, {"id": "u-123", "age": "thirty"}, spec)
    assert res_fail_type["verdict"] == "FAILED"

def test_api_contract_drift_and_ui_trace():
    engine = APITestingEngine()
    spec = {
        "openapi": "3.0.3",
        "info": {"title": "App API", "version": "1.0.0"},
        "paths": {
            "/api/v1/status": {
                "get": {"responses": {"200": {"description": "OK"}}}
            }
        }
    }

    traffic = [
        {"method": "GET", "path": "/api/v1/status", "status": 200, "body": {}},
        {"method": "POST", "path": "/api/v1/unmapped_endpoint", "status": 200, "body": {}}
    ]
    drift = engine.detect_contract_drift(traffic, spec)
    assert drift["drift_detected"] is True
    assert any("/api/v1/unmapped_endpoint" in e for e in drift["undocumented_endpoints"])

    # UI trace
    trace = engine.trace_ui_to_api(
        {"ui_element": "BuyButton", "endpoint": "/api/v1/status", "method": "GET", "status": 200, "latency_ms": 120.0},
        spec=spec
    )
    assert trace["contract_valid"] is True
    assert trace["latency_acceptable"] is True

def test_database_ddl_and_erd():
    engine = DatabaseEngine()
    ddl = """
    CREATE TABLE accounts (
        id VARCHAR(36) PRIMARY KEY,
        owner_name VARCHAR(100) NOT NULL
    );
    CREATE TABLE portfolios (
        id VARCHAR(36) PRIMARY KEY,
        account_id VARCHAR(36),
        FOREIGN KEY (account_id) REFERENCES accounts(id)
    );
    CREATE UNIQUE INDEX idx_acc_owner ON accounts(owner_name);
    """

    schema = engine.parse_sql_ddl(ddl)
    assert "accounts" in schema["tables"]
    assert "portfolios" in schema["tables"]
    assert schema["tables"]["accounts"]["primary_keys"] == ["id"]
    assert len(schema["tables"]["portfolios"]["foreign_keys"]) == 1
    assert len(schema["indexes"]) == 1

    mermaid = engine.generate_mermaid_erd(schema)
    assert "erDiagram" in mermaid
    assert "accounts" in mermaid
    assert "portfolios" in mermaid

    drawio = engine.generate_drawio_xml(schema)
    assert "<mxGraphModel" in drawio
    assert "accounts" in drawio

def test_database_migration_safety():
    engine = DatabaseEngine()

    safe_sql = "ALTER TABLE users ADD COLUMN nickname VARCHAR(50);"
    safe_res = engine.verify_migration_safety(safe_sql)
    assert safe_res["safe"] is True
    assert safe_res["status"] == "APPROVED"

    dangerous_sql = """
    DROP TABLE customer_balances;
    ALTER TABLE users DROP COLUMN email;
    ALTER TABLE users ADD COLUMN phone VARCHAR(20) NOT NULL;
    """
    danger_res = engine.verify_migration_safety(dangerous_sql)
    assert danger_res["safe"] is False
    assert danger_res["status"] == "REJECTED"
    assert danger_res["hazards_count"] >= 3

def test_database_schema_drift():
    engine = DatabaseEngine()
    expected_models = {
        "tables": {
            "users": {"columns": {"id": {"type": "VARCHAR"}, "email": {"type": "VARCHAR"}, "is_active": {"type": "BOOLEAN"}}}
        }
    }
    live_schema = {
        "tables": {
            "users": {"columns": {"id": {"type": "VARCHAR"}, "email": {"type": "VARCHAR"}}},
            "old_logs": {"columns": {"id": {"type": "INTEGER"}}}
        }
    }

    drift = engine.detect_schema_drift(expected_models, live_schema)
    assert drift["drift_detected"] is True
    assert any("is_active" in m for m in drift["column_mismatches"])
    assert "old_logs" in drift["extra_tables"]
