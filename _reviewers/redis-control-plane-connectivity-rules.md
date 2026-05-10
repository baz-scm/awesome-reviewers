---
title: Control-plane connectivity rules
description: Define a single, deterministic networking contract between data-plane
  nodes and the control plane (TD/FC), and make it resilient to CP reachability and
  multi-FC state consistency.
repository: redis/redis
label: Networking
language: Markdown
comments_count: 3
repository_stars: 74261
---

Define a single, deterministic networking contract between data-plane nodes and the control plane (TD/FC), and make it resilient to CP reachability and multi-FC state consistency.

Apply these rules:
1) **Minimize DP discovery/knowledge**: Data-plane code should not need to discover TD/FC addresses/locations. Prefer a design where the control plane learns ownership and connects/publishes to the assigned nodes, so the data plane only speaks a stable “FC-facing” protocol endpoint.
2) **Choose connection ownership intentionally**: If DP→CP, the control plane must rate-limit/jitter/retry to prevent thundering herd. If CP→DP, ensure DP listens on a well-defined port and accepts long-lived connections.
3) **Implement explicit “CP unreachable” behavior**: When a node can’t reach its owning FC for *X* seconds, it must stop serving all traffic or at least stop writes, based on configuration (e.g., `cluster-allow-reads-during-cluster-down`).
4) **Propagate routing-relevant state across FCs**: In a multi-FC deployment, ensure that failover/topology changes that affect how clients get slot routing (e.g., `CLUSTER SLOTS` / MOVED behavior) are visible to the FCs that serve those clients; otherwise different FCs will return conflicting views.

Example (CP-unreachable gating):
```pseudo
onHeartbeatTimeout():
  if timeSinceLastContact(owningFC) >= FC_UNREACHABLE_TIMEOUT:
    if clusterAllowReadsDuringClusterDown:
      blockWrites()
    else:
      stopServingAllTraffic()
```

These constraints keep the data plane’s networking simple, reduce overload risk on the control plane, and prevent stale routing answers across FC boundaries.