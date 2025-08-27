---
title: network topology plugin configuration
description: When implementing network topology-aware scheduling, ensure that the
  appropriate topology plugins are properly configured for different scheduling modes.
  In hard mode, the scheduler should strictly enforce topology constraints, while
  in soft mode, it should prefer network locality but allow cross-topology scheduling
  when necessary.
repository: volcano-sh/volcano
label: Networking
language: Go
comments_count: 2
repository_stars: 4899
---

When implementing network topology-aware scheduling, ensure that the appropriate topology plugins are properly configured for different scheduling modes. In hard mode, the scheduler should strictly enforce topology constraints, while in soft mode, it should prefer network locality but allow cross-topology scheduling when necessary.

For hard mode scheduling, verify that jobs are constrained to single hypernodes or tiers as specified:
```go
job := &e2eutil.JobSpec{
    Name: "topology-job",
    NetworkTopology: &batchv1alpha1.NetworkTopologySpec{
        Mode:               batchv1alpha1.HardNetworkTopologyMode,
        HighestTierAllowed: ptr.To(1),
    },
    // ... task specifications
}
```

For soft mode testing, enable the `network-topology-aware` plugin in the scheduler configuration to ensure pods within the same job are co-located when possible:
```yaml
# volcano-scheduler-ci.conf
plugins:
  - name: network-topology-aware
    enabledHierarchy: "*"
```

When designing test scenarios, ensure resource requests and cluster topology accurately reflect the intended scheduling behavior. For multi-tier scenarios, configure sufficient resource pressure to force scheduling across tiers while maintaining network locality preferences. This prevents tests from passing due to unrelated factors like bin-packing algorithms rather than proper topology awareness.