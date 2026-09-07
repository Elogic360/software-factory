# Scaling & Capacity Plan: QuantumVault Ledger Engine

**Document ID:** SCL-QV-001  
**Version:** 1.0.0  
**Status:** Production Target  
**Parent PRD:** PRD-QV-001  
**Parent Architecture:** ARC-PROJ-QV-001  
**Target Specification:** SPEC-QUANTUM-VAULT-2026  
**Lead Performance Engineer:** Principal Performance Engineer  
**Last Updated:** 2026-09-07  

---

## 1. Applicability Threshold & Scale Trigger

### 1.1 Mandatory Scaling Plan Rule
This document is **MANDATORY** for QuantumVault because:
1. **Target Concurrency:** Peak throughput is projected at `1,200 RPS` in Stage 1 and `10,000 RPS` in Stage 2 (exceeds the 500 RPS mandatory threshold).
2. **High Availability:** Operates across multi-AZ active-active deployment topologies.
3. **Strict Sub-150ms Latency Requirement:** High database write concurrency requires explicit read replica pooling and memory sharding.

---

## 2. Capacity Baseline & Growth Projections

| Metric Parameter | Baseline (MVP) | Stage 1 (10x Growth) | Stage 2 (Enterprise Scale) |
|------------------|----------------|----------------------|----------------------------|
| Daily Active Users (DAU) | 1,000 operators | 25,000 operators | 250,000 operators |
| Peak Requests Per Second (RPS) | 50 RPS | 1,200 RPS | 10,000 RPS |
| Total Stored Data Volume | 50 GB | 1.2 TB | 15 TB |
| Concurrent WebSocket Sessions | 200 sessions | 5,000 sessions | 50,000 sessions |

---

## 3. Bottleneck Analysis by Architectural Layer

### 3.1 Database & Persistence Tier
- **Bottleneck Risk:** Row-lock contention on account balances during high-frequency parallel settlements.
- **Symptom:** Transaction rollback spikes due to serialization failures (`40001 serialization_failure`).
- **Mitigation:**
  - Dynamic partition sharding by account range.
  - Read-heavy queries offloaded to read replica pool behind `pgBouncer`.
  - Monthly table partitioning for `audit_logs` and historical ledger entries.

### 3.2 Backend API & Compute Tier
- **Bottleneck Risk:** CPU saturation during Ed25519 token cryptographic verification.
- **Symptom:** API p95 latency exceeds 150ms ceiling.
- **Mitigation:**
  - In-memory public key validation cache.
  - Horizontal Pod Autoscaler (HPA) configured from 3 to 24 pods triggered at 70% CPU threshold.

### 3.3 Network & Ingestion Tier
- **Bottleneck Risk:** File descriptor exhaustion from 50,000 concurrent WebSocket connections.
- **Mitigation:** Epoll kernel parameter tuning (`sysctl -w fs.file-max=2097152`), Redis pub/sub broker sharding.

---

## 4. Horizontal vs. Vertical Scaling Strategy

| Component | Scaling Strategy | Scaling Trigger | Target Limits |
|-----------|------------------|-----------------|---------------|
| **API Gateway** | Horizontal | Ingress connections > 5,000 | 2 -> 8 instances |
| **Backend API Pods** | Horizontal (HPA) | CPU > 70% or Memory > 75% | 3 -> 24 pods |
| **Settlement Workers** | Horizontal | Queue length > 250 jobs | 2 -> 16 pods |
| **Primary PostgreSQL** | Vertical + Read Replicas | CPU > 65% or IOPS > 80% | 4 vCPU/16GB -> 16 vCPU/64GB + 3 Replicas |
| **Redis Cache Cluster** | Horizontal (Cluster Sharding) | Memory > 75% maxmemory | 3 nodes -> 6 node cluster |

---

## 5. Load Testing Benchmarks (Traceability from Testing Plan)

*Referenced from `TST-QV-001` load test suites:*
- **Sustained 500 RPS Benchmark:** P95 Latency = `88ms`, Error Rate = `0.00%` (PASSED).
- **Stress Limit Benchmark (Peak 2,500 RPS):** System degraded at `2,850 RPS` due to PostgreSQL connection pool exhaustion. Auto-scaling policy updated to scale read replicas at `1,500 RPS`.

---

## 6. Infrastructure Cost Projections by Scale Tier

| Infrastructure Tier | Target Scale | Monthly Cost Estimate (Cloud) | Key Cost Drivers |
|---------------------|--------------|-------------------------------|------------------|
| **Baseline Tier** | Up to 1k DAU / 50 RPS | ~$180 / month | 2 t4g.medium nodes, db.t4g.small, small Redis |
| **Growth Tier** | Up to 25k DAU / 1.2k RPS | ~$1,100 / month | 6 c6g.large pods, db.r6g.large + 2 Replicas, ElastiCache |
| **Enterprise Tier** | Up to 250k DAU / 10k RPS | ~$4,800 / month | 24+ c6g.xlarge pods, Aurora Multi-AZ, Redis cluster |

---

## 7. Signoff & Verification

- [x] Scale triggers and bottlenecks documented
- [x] Horizontal vs. vertical strategy evaluated per tier
- [x] Infrastructure cost curve analyzed
- [x] Approved by Principal Performance Engineer on 2026-09-07
