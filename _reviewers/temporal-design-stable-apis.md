---
title: Design stable APIs
description: 'When designing APIs, prioritize long-term stability and compatibility
  to avoid breaking changes. Use request/response objects pattern for methods that
  might evolve over time rather than direct parameters:'
repository: temporalio/temporal
label: API
language: Go
comments_count: 5
repository_stars: 14953
---

When designing APIs, prioritize long-term stability and compatibility to avoid breaking changes. Use request/response objects pattern for methods that might evolve over time rather than direct parameters:

```go
// Avoid - difficult to extend without breaking changes
func Terminate(ctx MutableContext, identity, reason string, details *commonpb.Payloads) error

// Prefer - allows adding fields without breaking existing clients
func Terminate(ctx MutableContext, request TerminateComponentRequest) (TerminateComponentResponse, error)
```

Be cautious when using protocol buffer messages in APIs, particularly with complex structures or oneoff fields that may cause serialization issues:

```go
// There are known issues with the default protobuf json converter when the message 
// contains oneoff fields - https://protobuf.dev/programming-guides/json/
// Consider using protojson to explicitly serialize/deserialize in such cases:
import "google.golang.org/protobuf/encoding/protojson"

// Explicit serialization for complex types
jsonBytes, err := protojson.Marshal(myProtoMessage)
```

Design semantically meaningful return types that reflect the logical structure of your data rather than implementation details:

```go
// Avoid returning raw indices
func getApproximateBacklogCount(subqueue int) int64

// Prefer returning a map keyed by meaningful values
func getApproximateBacklogCounts() map[int32]int64
```

When exposing interfaces, carefully consider which methods should be public. Expose only what external consumers need while keeping implementation details hidden to maintain flexibility for internal changes.