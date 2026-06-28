# Kubernetes Pre-Deployment Checklist

Run this checklist before deploying any service to a k8s cluster.

---

## Pre-Flight

- [ ] `kubectl cluster-info` — cluster is reachable
- [ ] `kubectl get nodes` — all nodes are Ready
- [ ] `kubectl get ns <namespace>` — target namespace exists
- [ ] Container image is built, tagged, and pushed to registry
- [ ] Image tag is immutable (no `latest` in production)
- [ ] Database migrations are backward-compatible

## Manifests

- [ ] Deployment has resource requests AND limits
- [ ] Deployment has liveness AND readiness probes
- [ ] Deployment has startupProbe if startup takes >30s
- [ ] Service selector matches deployment pod labels
- [ ] Ingress/Route is configured with correct host/path
- [ ] ConfigMap/Secret keys are correct and exist in namespace
- [ ] RBAC: ServiceAccount has minimum required permissions
- [ ] NetworkPolicy allows ingress from gateway and egress to DBs

## Security

- [ ] No secrets hardcoded in manifests or images
- [ ] Container runs as non-root user
- [ ] Container has readOnlyRootFilesystem where possible
- [ ] PodSecurityPolicy/Standards enforced
- [ ] Image scanning passed (Trivy/Snyk)

## Reliability

- [ ] PDB (PodDisruptionBudget) configured for HA services
- [ ] Anti-affinity rules for multi-replica deployments
- [ ] HPA configured for stateless services
- [ ] Graceful shutdown: terminationGracePeriodSeconds set
- [ ] PreStop hook for connection draining

## Rollback Plan

- [ ] Previous image tag documented
- [ ] Rollback command prepared: `kubectl rollout undo deployment/<name>`
- [ ] Database migration has rollback SQL
- [ ] Feature flags allow disabling new code without rollback

## Post-Deploy Verification

- [ ] `kubectl rollout status deployment/<name>` — rollout succeeded
- [ ] `kubectl get pods` — all pods Running and Ready
- [ ] `kubectl logs --tail=20` — no errors in startup
- [ ] Health endpoint returns 200
- [ ] Smoke test: core API endpoints respond correctly
- [ ] Monitor dashboards: no spike in error rate or latency
