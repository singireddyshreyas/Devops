# Session 12: Ingress, ConfigMaps and Secrets

This session demonstrates application configuration, Kubernetes Secret
consumption, Ingress routing and troubleshooting. Each lab is independent;
use a cluster with the required Ingress controller for the Ingress exercises.

## ConfigMap

Use the [`01-configmap/`](./01-configmap/) example to create non-sensitive
configuration and inject it into a Pod:

```bash
kubectl apply -f 01-configmap/app-config.yaml
kubectl get configmap
kubectl describe configmap <configmap-name>
```

Verify the injected environment values or mounted files from inside the
application container.

## Secret

Use [`02-secret/`](./02-secret/) to create a Secret and consume its keys from
a Pod:

```bash
kubectl apply -f 02-secret/db-secret.yaml
kubectl get secrets
kubectl describe secret <secret-name>
```

Base64 encoding is not encryption. Never commit real passwords, tokens,
private keys or production Secret values to Git. The checked-in values in
this exercise are placeholders for learning only; create real lab values
locally or use a secret manager, and do not print them in logs or screenshots.

## Ingress and Ingress Controller

Apply an application and Service before applying an Ingress:

```bash
kubectl apply -f 03-ingress/path-based.yml
kubectl get ingress
kubectl describe ingress <ingress-name>
```

An **Ingress** is a Kubernetes API resource that declares HTTP(S) host and
path routing rules. An **Ingress Controller** is the running implementation
that watches those resources and configures a proxy/load balancer to enforce
the rules. The resource alone does not route traffic; a compatible controller
must be installed, running and selected by the class/configuration.

For the full Minikube walkthrough, use
[`04-full-demo/README.md`](./04-full-demo/README.md). It covers ConfigMap and
Secret injection, frontend/backend Services, path routing and cleanup.

## Troubleshooting lab

Use the manifests and investigation process in
[`troubleshooting/`](./troubleshooting/):

1. Apply the broken resource and record its status.
2. Inspect it with `kubectl describe` and read Events.
3. Identify the root cause before changing the manifest.
4. Apply the fix and verify the resource and application connectivity.
5. Record actual before/after output; redact sensitive values.

Useful commands:

```bash
kubectl get pods,services,ingress
kubectl describe pod <pod-name>
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl logs <pod-name>
kubectl get endpoints <service-name>
```

Do not claim successful cluster execution from the example output in a lab
guide; capture the output from your own cluster.

## Terminal proof

The captured command parsed all 13 YAML files in this session. It checks
manifest syntax only; ConfigMap, Secret and Ingress behavior requires a live
cluster and is not represented as deployed here.

![Session 12 terminal validation](./proofs/terminal-validation.png)

### Local command run

From this session directory, `kubectl apply -f 01-configmap/app-config.yaml
--request-timeout=2s` failed validation because the Minikube API server was
unavailable (`context deadline exceeded`). ConfigMap, Secret and Ingress
operations were not applied. The Ingress example was not attempted because
the cluster is unavailable; no cloud resources or credentials were used.
