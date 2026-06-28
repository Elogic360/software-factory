# Kubernetes Operations Skill

Operate, deploy, debug, and scale containerized workloads on Kubernetes (k8s). Covers local (MicroK8s, kind, minikube), cloud (EKS, GKE, AKS), and bare-metal clusters.

---

## When to Use

- User says "deploy", "k8s", "kubernetes", "pod", "service", "ingress", "helm"
- User asks about scaling, rolling updates, canary deploys, blue-green
- Debugging pod failures, CrashLoopBackOff, OOMKilled, ImagePullBackOff
- Resource management: requests, limits, HPA, VPA, PDB
- Secrets management, ConfigMaps, environment injection
- Network policies, service mesh, mTLS
- CI/CD pipeline integration with k8s (GitHub Actions, ArgoCD)
- Monitoring: Prometheus ServiceMonitor, Grafana dashboards, alerting

---

## Prerequisites

- `kubectl` installed and configured (`~/.kube/config`)
- Cluster access confirmed: `kubectl cluster-info`
- Namespace understanding: always use project-specific namespaces

---

## Core Workflow

### 1. Cluster Inspection

```bash
# Cluster status
kubectl cluster-info
kubectl get nodes -o wide

# All resources in namespace
kubectl get all -n <namespace>

# Pod details (crash debugging)
kubectl describe pod <pod-name> -n <namespace>

# Live logs
kubectl logs <pod-name> -n <namespace> -f --tail=100

# Previous container logs (crash investigation)
kubectl logs <pod-name> -n <namespace> --previous
```

### 2. Deployment

```bash
# Apply manifests
kubectl apply -f deployment.yaml -n <namespace>

# Rollout status
kubectl rollout status deployment/<name> -n <namespace>

# Rolling update
kubectl set image deployment/<name> <container>=<new-image>:<tag> -n <namespace>

# Rollback
kubectl rollout undo deployment/<name> -n <namespace>
kubectl rollout history deployment/<name> -n <namespace>
```

### 3. Scaling

```bash
# Manual scale
kubectl scale deployment/<name> --replicas=3 -n <namespace>

# Autoscaler (HPA)
kubectl autoscale deployment/<name> --min=2 --max=10 --cpu-percent=70 -n <namespace>

# HPA from YAML
kubectl apply -f hpa.yaml -n <namespace>
```

### 4. Secrets & Config

```bash
# Create from literal
kubectl create secret generic my-secret --from-literal=key=value -n <namespace>

# Create from file
kubectl create secret generic tls-secret --from-file=tls.crt --from-file=tls.key -n <namespace>

# Create ConfigMap
kubectl create configmap my-config --from-file=config.yaml -n <namespace>

# Check secrets (base64)
kubectl get secret my-secret -n <namespace> -o jsonpath='{.data.key}' | base64 -d
```

### 5. Debugging

```bash
# Pod exec
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh

# Debug with ephemeral container
kubectl debug <pod-name> -it --image=busybox -n <namespace>

# Port forward (access internal service locally)
kubectl port-forward svc/<service-name> 8080:80 -n <namespace>

# Check events (errors, warnings)
kubectl get events -n <namespace> --sort-by=.lastTimestamp

# Resource usage
kubectl top nodes
kubectl top pods -n <namespace>
```

---

## Integral Market K8s Manifests

This project has k8s manifests at:
- `services/mt5-pod-controller/k8s/deployment.yaml` — MT5 pod controller
- `services/mt5-pod-controller/k8s/namespace.yaml` — Namespace definition
- `services/mt5-pod-controller/k8s/rbac.yaml` — ServiceAccount + Role + Binding
- `services/mt5-pod-controller/k8s/gc-cronjob.yaml` — Garbage collection cronjob

### Key patterns in this codebase:
- **1 pod = 1 MT5 terminal** (isolated Wine + Python process)
- **Namespace isolation** per trading node
- **RBAC** for pod controller to manage MT5 pods
- **CronJob** for garbage collection of stale pods

---

## Helm Best Practices

```bash
# Install chart
helm install <release> <chart> -n <namespace> -f values.yaml

# Upgrade
helm upgrade <release> <chart> -n <namespace> -f values.yaml

# Rollback
helm rollback <release> <revision> -n <namespace>

# Diff before apply
helm diff upgrade <release> <chart> -n <namespace> -f values.yaml
```

---

## Resource Management Template

```yaml
resources:
  requests:
    cpu: "250m"      # 0.25 CPU cores
    memory: "256Mi"  # 256 MiB RAM
  limits:
    cpu: "1000m"     # 1 CPU core
    memory: "512Mi"  # 512 MiB RAM
```

### Right-sizing guide:
| Workload | CPU Request | Memory Request | CPU Limit | Memory Limit |
|----------|------------|---------------|-----------|-------------|
| FastAPI backend | 250m | 256Mi | 1000m | 512Mi |
| Redis | 100m | 128Mi | 500m | 256Mi |
| PostgreSQL | 500m | 1Gi | 2000m | 4Gi |
| MT5 Terminal (Wine) | 500m | 512Mi | 2000m | 2Gi |
| Celery Worker | 250m | 256Mi | 1000m | 1Gi |

---

## Health Checks

### Liveness Probe
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3
```

### Readiness Probe
```yaml
readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
  failureThreshold: 3
```

### Startup Probe (slow-starting containers)
```yaml
startupProbe:
  httpGet:
    path: /health
    port: 8000
  failureThreshold: 30
  periodSeconds: 10
```

---

## Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-only-gateway
spec:
  podSelector:
    matchLabels:
      app: expert-backend
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: kong-gateway
    ports:
    - port: 8001
  policyTypes:
  - Ingress
```

---

## GitOps with ArgoCD

```bash
# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Create application
argocd app create my-app \
  --repo https://github.com/Elogic360/integralMarket \
  --path deploy/k8s \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace integral-market

# Sync
argocd app sync my-app
```

---

## Monitoring Stack

### Prometheus ServiceMonitor
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: backend-monitor
spec:
  selector:
    matchLabels:
      app: integral-market
  endpoints:
  - port: http
    path: /metrics
    interval: 15s
```

### Grafana Dashboard Import
1. Grafana → Dashboards → Import
2. Use pre-built dashboards:
   - Kubernetes Cluster Monitoring (ID: 7249)
   - FastAPI Monitoring (custom, ID: TBD)
   - PostgreSQL Database (ID: 11819)
   - Redis Dashboard (ID: 763)

---

## Common Issues & Fixes

| Issue | Symptom | Fix |
|-------|---------|-----|
| CrashLoopBackOff | Pod restarts repeatedly | `kubectl logs --previous`, check OOM, fix code error |
| ImagePullBackOff | Can't pull image | Check image name, tag, registry credentials, network |
| OOMKilled | Pod killed by kernel | Increase memory limits, fix memory leak |
| Pending pods | Cluster lacks resources | Check node resources, add nodes, or reduce requests |
| DNS failures | Service unreachable | Check CoreDNS pods, network policies |
| PVC stuck | Storage not provisioning | Check StorageClass, PVC status, node disk |
| RBAC denied | Forbidden errors | Check ServiceAccount, Role, RoleBinding |

---

## Reference Documents

- `references/deployment-checklist.md` — Pre-deployment verification steps
- `references/helm-patterns.md` — Helm chart patterns for this project
- `references/debugging-playbook.md` — Step-by-step debugging flows
- `references/scaling-strategies.md` — HPA, VPA, cluster autoscaler, MT5 pod scaling
