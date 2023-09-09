# Management (RKE) Cluster

## Bootstrapping a new Rancher RKE Cluster

In order to bootstrap a new `rancher-test/prodX` management plane, where Rancher GUI will be installed,
you have to use:

```bash
./bin/setup_rke install ....
```

which will setup nodes for RKE cluster.

## 1. Upgrade RKE to a new k8s version

Task: For a given RKE cluster, which has secrets stored in `git` repository,
we need to upgrade it to the newest K8s version, as per RKE binary.

```bash
./bin/setup_rke upgrade -d rancher-t2 -k "v1.20.11-rancher1"
```

What happens behind the scenes is following:

- secrets from git repo for `rancher-test2` are fetched, and `rancher-test2_rke_cluster.tar` content is extracted to `~/`.
  - See `rancher-config.yml` and `rancher-config.rkestate`
- Only if installing new RKE cluster: Using `bin/rke_template.py`, a `rancher-config.yml` is updated with a new k8s version.
- Next, RKE binary is applied with parameter `up`, see `rke up -h`.
- Secrets are updated (!) and hence will be encrypted and committed again
