# Kubernetes Workload and Service Object Comparison

## Deployment vs ReplicaSet

| Concern | Deployment | ReplicaSet |
| --- | --- | --- |
| Purpose | Declares the desired state for a stateless application and manages releases | Keeps a matching number of Pods running |
| Pod management | Creates and manages ReplicaSets, which create the Pods | Creates replacement Pods that match its selector and replica count |
| Scaling | Changes the desired replica count and coordinates the rollout | Changes the number of matching Pods |
| Rolling updates | Provides declarative updates, rollout status, history and rollback | Does not provide a rollout history or manage application revisions |
| Relationship | Owns the ReplicaSets for its revisions | Usually managed by a Deployment rather than edited directly |

Use a Deployment for ordinary stateless applications. It provides a safer
interface for scaling and updating than managing a ReplicaSet directly.

## Deployment vs DaemonSet vs StatefulSet

| Concern | Deployment | DaemonSet | StatefulSet |
| --- | --- | --- | --- |
| Typical use | Stateless web/API workloads | Node-level agents such as log or metrics collectors | Stateful workloads that need stable identity or storage |
| Pod placement | Schedules the requested number of interchangeable Pods | Schedules a Pod on each eligible node | Manages Pods with stable, ordered identities |
| Scaling | Set an arbitrary replica count | Usually scales with eligible nodes | Scale replicas while preserving ordinal identity |
| Networking | Normally accessed through a Service | Uses ordinary Pod networking; a Service may expose the agent | Often paired with a headless Service for stable DNS |
| Storage | May use shared or per-Pod claims, depending on the workload | Usually node-local or agent configuration | Can create a separate persistent volume claim per Pod |
| Examples | Frontend, API server | Node exporter, log collector | Database or clustered system requiring stable identity |

## ReplicaSet vs Service

These objects solve different problems:

- A **ReplicaSet** creates replacement Pods to maintain a desired count.
- A **Service** provides a stable virtual address and routes connections to
  ready Pods matching its selector.
- A Service is needed because Pod IPs can change when Pods are replaced.
- Traffic reaches Pods when the Service selector matches their labels and
  their readiness checks pass; inspect the resulting Endpoints or
  EndpointSlices to verify that selection.

Useful checks:

```bash
kubectl get pods --show-labels
kubectl get service
kubectl describe service <service-name>
kubectl get endpoints <service-name>
kubectl get endpointslices
```
