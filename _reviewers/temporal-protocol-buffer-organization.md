---
title: Protocol buffer organization
description: 'When defining protocol buffer messages, prioritize good organization
  and reuse:


  1. Reuse existing message types instead of duplicating structures. This reduces
  maintenance effort and prevents potential bugs from diverging implementations.'
repository: temporalio/temporal
label: Code Style
language: Other
comments_count: 2
repository_stars: 14953
---

When defining protocol buffer messages, prioritize good organization and reuse:

1. Reuse existing message types instead of duplicating structures. This reduces maintenance effort and prevents potential bugs from diverging implementations.

2. Group related fields together and maintain consistent field ordering throughout your protocol definitions. When fields are conceptually related (like `pass` and `id`), they should always appear together and in the same order.

Example:
```protobuf
// GOOD: Reusing existing message types
message TaskQueueUserData {
  api.temporal.server.v1.RateLimit rate_limit = 1;
}

// GOOD: Related fields grouped together in consistent order
message GetTaskQueueTasksRequest {
  int64 min_pass = 5;  // Related fields grouped together
  int64 min_task_id = 6;
  // Other fields...
}
```