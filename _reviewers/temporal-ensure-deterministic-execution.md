---
title: Ensure deterministic execution
description: "When working with Temporal workflows, maintaining deterministic behavior\
  \ is critical for reliable replay and execution across distributed systems. \n\n\
  Key practices:"
repository: temporalio/temporal
label: Temporal
language: Go
comments_count: 4
repository_stars: 14953
---

When working with Temporal workflows, maintaining deterministic behavior is critical for reliable replay and execution across distributed systems. 

Key practices:

1. **Use deterministic time sources**: Prefer values from requests or events over environment time when processing workflow logic. This ensures consistency during replay and across different clusters.

```go
// Instead of this:
now := env.Now()
nowpb := timestamppb.New(now)

// Prefer this when possible:
now := request.GetTriggerTime().AsTime()
nowpb := timestamppb.New(now)
```

2. **Account for clock skew**: When using time comparisons for task execution, use helper functions that account for potential time differences between systems.

```go
// Instead of directly comparing times:
if t.Now().After(deadline) { ... }

// Use utilities that handle skew:
if queues.IsTimeExpired(deadline, t.Now()) { ... }
```

3. **Be careful with non-deterministic functions**: Common libraries may contain non-deterministic behavior. Verify that operations like proto.Equal are safe for workflow code or create deterministic alternatives.

4. **Maintain time consistency**: When passing time values between components, ensure they derive from the same source to avoid inconsistency in execution paths.

These practices ensure workflows execute consistently during replay, across different clusters in multi-region setups, and when recovering from failures.