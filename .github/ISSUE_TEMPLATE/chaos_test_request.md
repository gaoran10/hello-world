---
name: Chaos test request
about: Open a chaos test
title: 'Chaos test'
labels: type/chaos-test
assignees: ''
---
# Chaos Test

Create issue with tag type/chaos-test to create a new Pulsar cluster with specific version.

Currently, the default image is `streamnative/pulsar-all`

Set Pulsar image version here.
== Chaos Cluster Configurations ==
```
# streamnative/pulsar-all
IMAGE_VERSION: 2.10.0-rc-202111212205
```
== Chaos Cluster Configurations End ==

Create a new comment to add chaos-mesh experiments and run chaos test.
== Chaos Cluster Configurations ==
```
# streamnative/pulsar-all
CHAOS_EXP: POD_KILL, NETWORK_DEALY
NETWORK_DEALY_TIMES: 30ms
TEST_DURATION: 100min
```
== Chaos Cluster Configurations End ==
