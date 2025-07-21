---
title: Consistent naming patterns
description: 'Maintain consistent naming patterns across related components and services.
  When implementing equivalent functionality in different services, use identical
  field/method names. When naming related fields that form logical groupings, either:'
repository: temporalio/temporal
label: Naming Conventions
language: Other
comments_count: 4
repository_stars: 14953
---

Maintain consistent naming patterns across related components and services. When implementing equivalent functionality in different services, use identical field/method names. When naming related fields that form logical groupings, either:

1. Use a structured type to represent the concept, or
2. Apply consistent suffix/prefix patterns that clearly indicate relationships

For request/response objects:
- Match existing naming patterns in related services (e.g., `UpdateTaskQueueConfig` should match the equivalent in workflowservice)
- For nested request objects, use descriptive prefixes to avoid ambiguity (e.g., use `heartbeat_request` instead of `request`)

Example:
```proto
// GOOD: Consistent suffix pattern for related fields
int64 ack_level_pass = 4;
int64 ack_level_id = 2;

// BETTER: Using a structured type
message Level {
    int64 pass = 1;
    int64 id = 2;
}
Level ack_level = 2;

// BAD: Inconsistent naming pattern
int64 ack_level_pass = 4;
int64 ack_level = 2; // Should be ack_level_id
```

Consistent naming reduces cognitive load, improves readability, and helps prevent errors when working across service boundaries.