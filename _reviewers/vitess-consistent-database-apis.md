---
title: Consistent database APIs
description: Design database APIs with consistent patterns for response structures
  and error handling. Follow established conventions in your codebase, even when it
  means returning empty response objects for error-only operations.
repository: vitessio/vitess
label: Database
language: Other
comments_count: 2
repository_stars: 19815
---

Design database APIs with consistent patterns for response structures and error handling. Follow established conventions in your codebase, even when it means returning empty response objects for error-only operations.

For RPC or service endpoints:
1. Return structured response objects consistently, even when empty
2. Avoid duplicating fields across response structures
3. Maintain a predictable error handling pattern

**Example:**
```protobuf
// Good: Follows convention of always having a response message
message ValidatePermissionsKeyspaceRequest {
  string keyspace = 1;
  repeated string shards = 2;
}

message ValidatePermissionsKeyspaceResponse {
  // Even if initially empty, this maintains API consistency
  // and allows for future extension without breaking changes
}

// Avoid: Duplicating fields across structures
message StopReplicationAndGetStatusResponse {
  replicationdata.StopReplicationStatus status = 2;
  // Don't add backup_running here if it already exists in status
}
```

This pattern creates more maintainable database interfaces that can evolve without breaking changes, while keeping a consistent experience for developers consuming your API.