# Kubernetes Debugging Playbook

Step-by-step flows for the most common k8s failure scenarios.

---

## Flow 1: Pod CrashLoopBackOff

```
1. kubectl get pods -n <ns>                          → confirm CrashLoopBackOff
2. kubectl logs <pod> -n <ns> --previous             → see last crash output
3. kubectl describe pod <pod> -n <ns>                → check Events for OOM/image issues
4. kubectl top pods -n <ns>                          → check if OOM (memory near limit)
5. If OOM: increase memory limit OR fix leak
6. If code error: check application logs, fix, redeploy
7. kubectl rollout undo deployment/<name> -n <ns>    → rollback if needed
```

## Flow 2: Service Unreachable

```
1. kubectl get svc <name> -n <ns>                    → confirm Service exists
2. kubectl get endpoints <name> -n <ns>              → check if endpoints have IP:port
3. If no endpoints: selector mismatch → check pod labels vs svc selector
4. kubectl exec -it <test-pod> -- wget -qO- http://<svc-name>:<port>/health
5. Check NetworkPolicy: kubectl get networkpolicy -n <ns>
6. Check CoreDNS: kubectl -n kube-system logs -l k8s-app=kube-dns
```

## Flow 3: ImagePullBackOff

```
1. kubectl describe pod <pod> -n <ns>                → see image pull error
2. Common causes:
   - Wrong image name/tag → verify with docker inspect
   - Registry auth missing → create imagePullSecret
   - Network issue → check node internet connectivity
3. Fix: kubectl create secret docker-registry regcred \
   --docker-server=<registry> --docker-username=<user> --docker-password=<pass>
4. Add to deployment: spec.template.spec.imagePullSecrets: [{name: regcred}]
```

## Flow 4: Pending Pods

```
1. kubectl describe pod <pod> -n <ns>                → see Events
2. If "Insufficient cpu/memory": nodes lack resources
   - kubectl top nodes                              → check available
   - Reduce resource requests OR add nodes
3. If "No nodes match": nodeSelector/affinity mismatch
4. If "PersistentVolumeClaim pending": StorageClass issue
   - kubectl get sc                                 → check available StorageClasses
   - kubectl get pv                                 → check available PVs
```

## Flow 5: RBAC Denied (Forbidden)

```
1. kubectl auth can-i <verb> <resource> --as=system:serviceaccount:<ns>:<sa>
2. If no: need to add Role + RoleBinding
3. Create Role with minimum permissions
4. Create RoleBinding linking ServiceAccount → Role
5. Verify: kubectl auth can-i <verb> <resource> --as=system:serviceaccount:<ns>:<sa>
```

## Flow 6: MT5 Pod Specific Issues

```
1. kubectl logs <mt5-pod> -n trading                → check Wine startup
2. kubectl exec -it <mt5-pod> -- wineserver -k      → restart Wine if stuck
3. kubectl exec -it <mt5-pod> -- python -c "import metatrader5; print(mt5.__version__)"
4. Check MT5 gateway health: curl http://<gateway>:8099/health
5. If connection timeout: MT5 terminal not initialized → check Wine + Python setup
6. Garbage collection: kubectl get jobs -n trading   → check gc-cronjob runs
```

## Flow 7: Persistent Volume Issues

```
1. kubectl get pvc -n <ns>                          → check PVC status
2. If Pending: check StorageClass, node disk, provisioner
3. If Bound but pod can't mount: check access modes (RWO vs RWX)
4. If Lost: underlying PV deleted → recreate PV + PVC
5. Data recovery: check if backup exists (Velero, manual dump)
```

## Quick Diagnostic Commands

```bash
# Everything that's not running
kubectl get pods --all-namespaces | grep -v Running | grep -v Completed

# Recent events (sorted by time)
kubectl get events --all-namespaces --sort-by=.lastTimestamp | tail -30

# Resource usage across cluster
kubectl top nodes && kubectl top pods --all-namespaces

# Check all services and their endpoints
kubectl get svc,endpoints --all-namespaces

# Find which pod serves a service
kubectl get endpoints <service-name> -n <ns> -o yaml
```
