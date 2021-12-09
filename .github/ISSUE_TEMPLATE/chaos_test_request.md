---
name: Chaos test request
about: Open a chaos test
title: 'Chaos test streamnative/sn-platform:2.9.0.0-rc-6'
labels: ['chaos-test']
---

# Chaos Test

## 1. Create Pulsar cluster

Create an issue with tag type/chaos-test to create a new Pulsar cluster with a specific version.

Currently, the default image is `streamnative/sn-platform`

Set Pulsar image version here.
== Chaos Cluster Configurations ==
```
# streamnative/sn-platform
IMAGE_VERSION: 2.9.0.0-rc-6
```
== Chaos Cluster Configurations End ==

## 2. Add chaos-mesh and test

Create a new comment to add chaos-mesh experiments and run chaos test.
== Chaos Test Configurations ==
```
CHAOS_EXPS: POD_KILL, NETWORK_DELAY
CHAOS_PARAM_POD_KILL_CRON: */5 * * * *
CHAOS_PARAM_NETWORK_DELAY: */5 * * * *
NETWORK_DEALY_TIMES: 30ms
TEST_DURATION: 100min
EXTERNAL_SERVICE_DOMAIN: localhost
```
== Chaos Test Configurations End ==
