---
title: reuse common message types
description: Prefer reusable message types over single-purpose request/response pairs
  to reduce API bloat and improve maintainability. Avoid creating dedicated "Response"
  types when the return value can be a plain, reusable struct. Merge identical request
  types and leverage common message patterns like StringRequest or EmptyRequest where
  appropriate.
repository: cline/cline
label: API
language: Other
comments_count: 5
repository_stars: 48299
---

Prefer reusable message types over single-purpose request/response pairs to reduce API bloat and improve maintainability. Avoid creating dedicated "Response" types when the return value can be a plain, reusable struct. Merge identical request types and leverage common message patterns like StringRequest or EmptyRequest where appropriate.

Key principles:
- Return plain types that can be reused as structs in the codebase rather than RPC-specific response types
- Merge identical request types instead of creating duplicates for each RPC
- Use existing common message types (StringRequest, EmptyRequest) when the message structure matches
- Avoid anti-patterns like success/error fields in response types - let gRPC handle errors

Example:
```protobuf
// Avoid: Single-use response type
rpc getRecordingStatus(GetRecordingStatusRequest) returns (GetRecordingStatusResponse);

// Prefer: Reusable plain type
rpc getRecordingStatus(EmptyRequest) returns (RecordingStatus);

// Avoid: Duplicate request types
message RestartMcpServerRequest {
  Metadata metadata = 1;
  string server_name = 2;
}

// Prefer: Reuse common type
rpc restartMcpServer(StringRequest) returns (Empty);
```

This approach creates cleaner APIs with fewer message types while maintaining the same functionality.