---
title: Safe lock patterns
description: When implementing concurrent operations, ensure locks are acquired and
  released properly in all execution paths. Always use patterns that guarantee lock
  release, and document lock acquisition order to prevent deadlocks.
repository: opentofu/opentofu
label: Concurrency
language: Go
comments_count: 6
repository_stars: 25901
---

When implementing concurrent operations, ensure locks are acquired and released properly in all execution paths. Always use patterns that guarantee lock release, and document lock acquisition order to prevent deadlocks.

**Key practices:**

1. **Always release locks on all return paths** - Use defer statements for cleanup to guarantee locks are released even on error paths:

```go
func (d *Dir) InstallPackage(ctx context.Context, meta getproviders.PackageMeta) error {
    unlock, err := d.Lock(ctx, meta.Provider, meta.Version)
    if err != nil {
        return err
    }
    defer unlock() // Ensures lock is released on all return paths
    
    // Implementation...
}
```

2. **Document lock acquisition order** - When acquiring multiple locks, establish and document a consistent order to prevent deadlocks:

```go
// Acquire locks in consistent order: s3 first, then dynamoDB
s3LockId, err := c.s3Lock(info)
if err != nil {
    return "", err
}
dynamoLockId, err := c.dynamoDbLock(info)
if err != nil {
    return "", err
}
```

3. **Use explicit synchronization patterns** - When coordinating multiple concurrent operations, use clear patterns with channels and wait groups:

```go
lockResults := make(chan lockResult, len(platforms))
go func() {
    var wg sync.WaitGroup
    for _, platform := range platforms {
        wg.Add(1)
        go func(platform getproviders.Platform) {
            // Process work
            lockResults <- result
            wg.Done()
        }(platform)
    }
    wg.Wait()
    close(lockResults)
}()

for result := range lockResults {
    // Process results
}
```

4. **Handle concurrent error cases** - When operating with multiple locks, handle partial failure cases explicitly by cleaning up already acquired resources.

Following these patterns helps prevent race conditions, deadlocks, and resource leaks in concurrent code.