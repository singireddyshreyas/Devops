# TaskBoard GitOps

This folder contains an Argo CD Application that watches the TaskBoard Helm
chart in this repository. Git is the desired-state source; Argo CD compares
that state with the cluster and reconciles drift.

## Before syncing

1. Merge the TaskBoard chart and tested container image changes into the
   repository's `main` branch.
2. Set both image tags in `taskboard-application.yaml` to the same tested
   commit SHA published to GHCR. Do not use a floating tag for a production
   deployment.
3. Create the namespace-scoped `taskboard-postgres-credentials` Secret and
   `ghcr-pull-secret` in the destination cluster using an approved secret
   delivery process. Do not add Secret values to Git or Helm parameters.
4. Ensure Argo CD can read this repository and the cluster has the required
   ingress controller, storage class and metrics provider.

The sample points to this repository. If you fork or move the project, update
`repoURL` to the repository you control.

## Install Argo CD and apply the Application

Install Argo CD using the official installation instructions for your
cluster, then apply the Application:

```bash
kubectl apply -f taskboard-application.yaml
kubectl get applications -n argocd
kubectl get pods -n taskboard
```

The chart creates the ConfigMap, frontend/backend/PostgreSQL workloads,
Services, probes, PVC, HPA and optional Ingress/ServiceMonitor. The database
credentials remain outside Git.

## Demonstrate reconciliation

After the app is Synced and Healthy, change a non-secret desired-state value
in the Helm chart or Application manifest, commit and push it, then observe
Argo CD sync the change. For drift demonstration, manually change a replica
count and observe self-heal restore the Git-declared value.

Delete the Application and clean up its namespace only after confirming that
you no longer need the application data.
