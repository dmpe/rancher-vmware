# Rancher VMware

This repository contains formerly firm's internal code which has been been used for setting up Rancher environment. 
Given migration to competitor's platform, it has been published here, in parts, in the :warning: non-working :warning: form. 

Many of the function cannot be published, and will need to be replaced with their equals. 

**Warning:** None of this has been ever properly tested here. Consider this more like PoC Code Snippets
which will require a lot of adjustments. 

See script file for some additional documentation.

## Overview of hostnames in k8s clusters

Website showing Rancher VM hostnames in the VMware Cluster, using exported data

To generate output, execute:

```
python3 gen.py
```

# Management (RKE) Cluster

## Bootstrapping a new Rancher RKE Cluster

In order to bootstrap a new `rancher-testX/prodX` management cluster, where Rancher GUI will be installed,
you have to use:

```bash
./bin/setup_rke install ....
```

which will setup nodes for RKE cluster.

## 1. Upgrade RKE to a new k8s version

For a given RKE cluster, which has secrets stored in `git` repository,
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
