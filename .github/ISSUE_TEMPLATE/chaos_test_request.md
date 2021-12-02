---
name: Chaos test request
about: Open a chaos test
title: 'Chaos test'
labels: ['chaos-test']
---

# Chaos Test

## 1. Create Pulsar cluster

Create an issue with tag type/chaos-test to create a new Pulsar cluster with a specific version.

Currently, the default image is `streamnative/pulsar-all`

Set Pulsar image version here.
== Chaos Cluster Configurations ==
```
# streamnative/pulsar-all
IMAGE_VERSION: 2.10.0-rc-202111212205
```
== Chaos Cluster Configurations End ==

## 2. Add chaos-mesh and test

Create a new comment to add chaos-mesh experiments and run chaos test.
== Chaos Test Configurations ==
```
# streamnative/pulsar-all
CHAOS_EXP: POD_KILL, NETWORK_DEALY
NETWORK_DEALY_TIMES: 30ms
TEST_DURATION: 100min
```
== Chaos Test Configurations End ==
