---
title: Use file locks
description: When multiple processes or goroutines need to access shared file system
  resources concurrently, use file locks (flock) to prevent race conditions and ensure
  mutual exclusion. This is particularly important for operations like certificate
  file management, directory creation, and other file system modifications that could
  conflict.
repository: snyk/cli
label: Concurrency
language: Go
comments_count: 2
repository_stars: 5178
---

When multiple processes or goroutines need to access shared file system resources concurrently, use file locks (flock) to prevent race conditions and ensure mutual exclusion. This is particularly important for operations like certificate file management, directory creation, and other file system modifications that could conflict.

Consider placing lock files in appropriate locations - for resources being created, use a lock file in an existing directory (like temp dir) rather than within the directory being created. This prevents the chicken-and-egg problem of needing to create a directory to place a lock file for that same directory creation.

Example approach:
```go
// For certificate file operations
if _, existsError := os.Stat(caSingleton.CertFile); errors.Is(existsError, fs.ErrNotExist) {
    // Any error should trigger regeneration, use file lock during creation
    // Set exclusive flock on cert file while process is running
}

// For directory creation with subdirectories
// Use flock in conjunction with MkdirAll, place lock file outside target directory
lockFile := filepath.Join(os.TempDir(), "cache-creation.lock")
// Acquire lock, then safely create directory structure
```

This pattern ensures that concurrent operations on shared file resources are properly synchronized and prevents corruption or inconsistent state.