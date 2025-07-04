---
title: Wrap errors with context
description: Always wrap errors with meaningful context using fmt.Errorf and %w verb.
  Include relevant identifiers (filenames, IDs, paths) in error messages to aid debugging.
  This helps pinpoint error sources and simplifies troubleshooting.
repository: influxdata/influxdb
label: Error Handling
language: Go
comments_count: 6
repository_stars: 30268
---

Always wrap errors with meaningful context using fmt.Errorf and %w verb. Include relevant identifiers (filenames, IDs, paths) in error messages to aid debugging. This helps pinpoint error sources and simplifies troubleshooting.

Example:
```go
// Bad:
if err := os.Open(path); err != nil {
    return err  // Original context is lost
}

// Good:
if err := os.Open(path); err != nil {
    return fmt.Errorf("failed to open config file %q: %w", path, err)
}

// Bad:
func (s *Store) SetShardNewReadersBlocked(shardID uint64, blocked bool) error {
    if sh == nil {
        return ErrShardNotFound  // Missing context
    }
}

// Good:
func (s *Store) SetShardNewReadersBlocked(shardID uint64, blocked bool) error {
    if sh == nil {
        return fmt.Errorf("shard not found: id=%d blocked=%v: %w", 
            shardID, blocked, ErrShardNotFound)
    }
}
```

Key points:
- Use fmt.Errorf with %w to wrap errors while preserving the error chain
- Include relevant identifiers (paths, IDs) in error messages
- Add operation context to clarify what failed
- Preserve the original error for error type checking with errors.Is()