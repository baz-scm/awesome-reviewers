---
title: maintain backward compatibility
description: When modifying existing APIs, preserve original parameter types and return
  signatures to avoid breaking client code. Even when internal implementations change
  or new functionality is added, the public interface should remain stable for existing
  consumers.
repository: golang/go
label: API
language: Go
comments_count: 2
repository_stars: 129599
---

When modifying existing APIs, preserve original parameter types and return signatures to avoid breaking client code. Even when internal implementations change or new functionality is added, the public interface should remain stable for existing consumers.

For example, when extending a Logger to support multiple outputs, maintain the original single-writer constructor:

```go
// Keep original API intact
func New(out io.Writer, prefix string, flag int) *Logger {
    // Internal implementation can adapt to new multi-writer design
}

// Add new functionality separately if needed
func NewMultiWriter(outs []io.Writer, prefix string, flag int) *Logger {
    // New API for enhanced functionality
}
```

Similarly, when changing return types, ensure the new type is compatible with existing usage patterns or maintain the original signature alongside new variants. This approach protects existing integrations while allowing API evolution.