---
title: Use testify assertions
description: Always use the testify package (require/assert) in tests instead of standard
  Go testing assertions. The testify library provides more descriptive failure messages
  that make debugging test failures easier and faster.
repository: influxdata/influxdb
label: Testing
language: Go
comments_count: 7
repository_stars: 30268
---

Always use the testify package (require/assert) in tests instead of standard Go testing assertions. The testify library provides more descriptive failure messages that make debugging test failures easier and faster.

Replace standard testing patterns with testify equivalents:

```go
// Instead of this:
if err := s.CreateShard("db0", "rp0", 1, true); err != nil {
    t.Fatal(err)
}
if len(s.Store.GetBadShardList()) != 0 {
    t.Fatalf("expected empty list, got %v", s.Store.GetBadShardList())
}
if !reflect.DeepEqual(expected, actual) {
    t.Fatalf("values don't match")
}

// Use these testify equivalents:
require.NoError(t, s.CreateShard("db0", "rp0", 1, true), "creating shard")
require.Empty(t, s.Store.GetBadShardList(), "bad shard list should be empty")
require.Len(t, s.Store.GetBadShardList(), 1, "should have exactly one bad shard")
require.Equal(t, expected, actual, "values should match")
```

Also use modern testing utilities for resource management:
- Use `t.TempDir()` instead of manual directory creation and cleanup
- Use `t.Cleanup()` for all resource cleanup instead of defer statements

These patterns make tests more maintainable, provide better error messages when tests fail, and ensure proper cleanup even when tests panic or fail early.