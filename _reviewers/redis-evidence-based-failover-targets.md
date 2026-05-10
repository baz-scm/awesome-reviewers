---
title: Evidence-Based Failover Targets
description: When proposing performance/SLA goals (e.g., failover completion time),
  require an evidence-based rationale and a repeatable way to validate them—especially
  for worst-case behavior.
repository: redis/redis
label: Performance Optimization
language: Markdown
comments_count: 2
repository_stars: 74261
---

When proposing performance/SLA goals (e.g., failover completion time), require an evidence-based rationale and a repeatable way to validate them—especially for worst-case behavior.

Apply this by documenting:
- Target definition: what exactly “10s failover” includes/excludes (detection, consensus/propagation, promotion, client-observable recovery).
- Worst-case assumptions: network latency bounds, timeouts, quorum/heartbeat intervals, failure model, and any upper bounds.
- Measurement basis: links to benchmarks/profiles or at least a structured summary of real-world observations (cloud regions/AZs, instance/network reliability stats).
- Acceptance tests: automated tests (or staging runs) that exercise the failure mode(s) producing the worst case and assert the target.

Example standard text developers can follow:
```text
Failover target: <=10s (worst-case), <=5s (some configs).
Definition: time from heartbeat timeout detection to topology+role update propagated to all impacted nodes, including client observable readiness.
Assumptions: cross-AZ RTT p99=..., heartbeat interval=..., coordinator tick=..., quorum=...
Evidence: benchmark/staging results in regions X/Y with injected failures; include traces/profiles.
Regression guard: CI/staging test fails if p99/worst-case exceeds target.
```

This ensures performance claims aren’t just experience-based anecdotes, and it prevents future changes from silently breaking latency guarantees.