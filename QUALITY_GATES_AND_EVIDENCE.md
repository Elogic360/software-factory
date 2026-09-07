# 🛡️ Quality Control Gates & Evidence Ledger (G0 - G15)

The manufacturing floor enforces 16 sequential quality gates. No stage can proceed without satisfying the prerequisite gate's evidence criteria:

| Gate | Name | Station | Required Evidence Artifact |
| :--- | :--- | :--- | :--- |
| **G0** | Product Accepted | Product Discovery | `PRD.md` |
| **G1** | Requirements Complete | Requirements | `REQUIREMENTS.md` |
| **G2** | Specification Approved | Specification | `SYSTEM_SPEC.md` |
| **G3** | Architecture Approved | Architecture | `ARCHITECTURE.md` |
| **G4** | Security Design Approved | Security Lab | `THREAT_MODEL.md` |
| **G5** | Implementation Plan Approved | Planning | `IMPLEMENTATION_PLAN.md` |
| **G6** | Production Complete | Production Floor | `WORK_ORDERS.json` |
| **G7** | Unit Tests Passed | QA Lab | `UNIT_TESTS.xml` |
| **G8** | Integration Tests Passed | QA Lab | `INTEGRATION_TESTS.json` |
| **G9** | E2E Passed | QA Lab | `E2E_REPORT.json` |
| **G10** | Security Passed | Security Lab | `SAST_REPORT.json` |
| **G11** | Performance Passed | Performance Lab | `LOAD_REPORT.json` |
| **G12** | Staging Passed | Test Ground | `STAGING_SIGNOFF.json` |
| **G13** | Release Candidate Approved | Release Control | `RC_VERDICT.json` |
| **G14** | Production Deployment | DevOps / SRE | `DEPLOYMENT_LOG.json` |
| **G15** | Production Health Confirmed | Observability | `HEALTH_TELEMETRY.json` |
