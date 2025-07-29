---
title: Document configuration constraints
description: Configuration documentation must explicitly specify when settings should
  or should not be used, including conditional requirements and mutually exclusive
  options. This prevents misconfigurations and helps developers understand the proper
  context for each setting.
repository: apache/kafka
label: Configurations
language: Html
comments_count: 2
repository_stars: 30575
---

Configuration documentation must explicitly specify when settings should or should not be used, including conditional requirements and mutually exclusive options. This prevents misconfigurations and helps developers understand the proper context for each setting.

When documenting configurations:
- Clearly state when a configuration should NOT be used
- Specify conditional requirements (e.g., "only applies when X is set")
- Explain mutually exclusive options
- Provide context about when settings are relevant

Example:
```
controller.quorum.voters - Map of id/endpoint information for static voters. 
This should NOT be set if using dynamic quorums. See Static versus Dynamic 
KRaft Quorums for details.

group.protocol=streams - Additional ACLs are required for the new Streams 
rebalance protocol only when group.protocol=streams is set in the configuration.
```

This approach ensures developers can quickly understand configuration boundaries and avoid common setup mistakes.