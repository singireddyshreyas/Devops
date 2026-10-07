# CoreDNS in Kubernetes

## What CoreDNS does

CoreDNS is the cluster DNS server used by Kubernetes. It answers DNS queries
for Services and, depending on cluster configuration, Pods and external
domains. Pods normally receive cluster DNS settings automatically.

## Service discovery and query resolution

The usual Service DNS name is:

```text
<service>.<namespace>.svc.<cluster-domain>
```

For example, a Service named `api` in namespace `production` is commonly
resolved as:

```text
api.production.svc.cluster.local
```

The cluster domain is configurable; `cluster.local` is common but is not a
guaranteed value. A query in the same namespace can usually use only the
Service name. A headless Service resolves to the addresses of its selected
Pods rather than a virtual ClusterIP. An `ExternalName` Service returns a
DNS alias to its configured external name.

At a high level, CoreDNS receives the Pod's DNS query, applies its Kubernetes
plugin to look up cluster records, and returns the corresponding answer.
Queries outside the cluster domain can be forwarded according to the
CoreDNS configuration.

## Inspect configuration

```bash
kubectl get pods -n kube-system
kubectl get configmap coredns -n kube-system -o yaml
kubectl describe deployment coredns -n kube-system
```

The CoreDNS ConfigMap typically contains the Corefile, which defines the
plugins and forwarding behavior. Do not edit a managed cluster's DNS
configuration without understanding the provider's supported workflow.

## Troubleshoot DNS

Run a disposable client Pod in the same namespace as the Service:

```bash
kubectl run dns-check --rm -it --restart=Never \
  --image=busybox:1.36 -- nslookup api.production.svc.cluster.local
```

Then check the namespace, Service, selector and endpoints:

```bash
kubectl get service api -n production
kubectl get pods -n production --show-labels
kubectl get endpoints api -n production
kubectl get endpointslices -n production
```

Check that CoreDNS Pods are ready and inspect their logs:

```bash
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns --all-containers=true
```

If DNS resolution fails, verify that the client Pod has the expected
`/etc/resolv.conf`, that the Service name and namespace are correct, that
CoreDNS has ready endpoints, and that network policies allow DNS traffic.
