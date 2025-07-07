---
title: Initialize before null-checking
description: When handling potentially nil values, ensure proper initialization order
  to prevent race conditions and null reference errors. This is critical for maintaining
  thread safety and following idiomatic Go patterns.
repository: gin-gonic/gin
label: Null Handling
language: Go
comments_count: 2
repository_stars: 83022
---

When handling potentially nil values, ensure proper initialization order to prevent race conditions and null reference errors. This is critical for maintaining thread safety and following idiomatic Go patterns.

For shared resources, acquire locks before performing null checks and initialization:

```go
// Good: Lock first to prevent race conditions
c.KeysLocker.Lock()
if c.Keys == nil {
    c.Keys = make(map[string]interface{})
}

// Problematic: May miss concurrent initialization
if c.Keys == nil {
    c.KeysLocker.Lock()
    c.Keys = make(map[string]interface{})
}
```

When checking for specific error types, declare target variables before using them:

```go
// Good: Declare before use
var maxBytesErr *http.MaxBytesError
if errors.As(err, &maxBytesErr) {
    // handle error
}

// Avoid: Creates unnecessary struct instance
maxBytesErr := &http.MaxBytesError{}
if errors.As(err, &maxBytesErr) {
    // handle error
}
```

This approach ensures proper resource handling, reduces memory allocation, and follows Go's conventions for null safety patterns.