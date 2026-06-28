# Kubernetes Scaling Strategies

Covers horizontal scaling, vertical scaling, cluster autoscaling, and workload-specific scaling for Integral Market.

---

## Horizontal Scaling (Scale Out)

### HorizontalPodAutoscaler (HPA)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: expert-backend-hpa
  namespace: integral-market
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: expert-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Pods
        value: 2
        periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Pods
        value: 1
        periodSeconds: 120
```

### When to use HPA:
- Stateless services (API backends, web servers)
- Services with variable load (trading hours vs off-hours)
- Services that can handle concurrent requests

### When NOT to use HPA:
- Stateful services (PostgreSQL, Redis) — use read replicas instead
- Single-instance services (MT5 Gateway) — 1 terminal = 1 pod
- Services with in-memory state that can't be distributed

---

## Vertical Scaling (Scale Up)

### VerticalPodAutoscaler (VPA)

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: expert-backend-vpa
  namespace: integral-market
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: expert-backend
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: expert-backend
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 4000m
        memory: 8Gi
      controlledResources: ["cpu", "memory"]
```

### When to use VPA:
- Databases with predictable but growing resource needs
- Services where right-sizing is unknown (start with VPA, switch to HPA later)
- Non-HA services where restart during scaling is acceptable

---

## Cluster Autoscaler

```yaml
# Cloud provider configuration varies:
# AWS EKS: eksctl or --cluster-autoscaler flag
# GKE: node auto-provisioning
# AKS: cluster autoscaler addon

# Min/max nodes
--min-nodes=3
--max-nodes=20
--scale-down-utilization-threshold=0.5
--scale-down-delay-after-add=10m
```

---

## Integral Market Scaling Playbook

| Service | Scaling Strategy | Min | Max | Trigger |
|---------|-----------------|-----|-----|---------|
| React SPA | N/A (static) | 1 | 1 | N/A (Cloudflare handles) |
| Kong Gateway | HPA | 2 | 4 | CPU > 70% |
| Market Backend | HPA | 2 | 6 | CPU > 70% |
| Expert Backend | HPA | 2 | 8 | CPU > 70%, queue depth |
| Intelligence | HPA | 2 | 4 | CPU > 70% |
| Sensei Backend | HPA | 1 | 3 | CPU > 70% |
| PostgreSQL | Read replicas | 1 | 3 | Query latency |
| Redis | Cluster mode | 1 | 3 | Memory > 70% |
| MT5 Gateway | Fixed | 1 | 1 | 1 terminal = 1 pod |
| Celery Workers | HPA | 1 | 5 | Queue depth > 100 |

---

## MT5 Pod Scaling (Special Case)

MT5 terminals are 1:1 with pods. Scaling is handled by the MT5 Pod Controller:

```bash
# Pod Controller scales based on:
1. Number of active MT5 accounts
2. Account priority (real money > demo)
3. Resource availability on nodes
4. Garbage collection of stale terminals

# Scale MT5 farm:
kubectl scale deployment mt5-pod-controller --replicas=3 -n trading
```

### Garbage Collection:
- CronJob runs every 6 hours
- Cleans up: crashed MT5 pods, stale connections, orphaned PVCs
- Config: `services/mt5-pod-controller/k8s/gc-cronjob.yaml`
