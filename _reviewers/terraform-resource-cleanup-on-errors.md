---
title: Resource cleanup on errors
description: Always ensure proper resource cleanup in error paths to prevent leaks.
  Use defer functions with explicit error checking for closing operations, and log
  any close errors that occur during cleanup.
repository: hashicorp/terraform
label: Error Handling
language: Go
comments_count: 4
repository_stars: 45532
---

Always ensure proper resource cleanup in error paths to prevent leaks. Use defer functions with explicit error checking for closing operations, and log any close errors that occur during cleanup.

When working with resources like file handles, network connections, or API responses, make sure to:

1. Use defer statements to guarantee cleanup even when errors occur
2. Check for and log errors that happen during the cleanup process itself
3. Use context-aware cancellation when appropriate

For example, instead of:

```go
getOutput, err := c.s3Client.GetObject(ctx, getInput)
if err != nil {
    return fmt.Errorf("unable to retrieve file: %w", err)
}
defer getOutput.Body.Close()
```

Prefer:

```go
getOutput, err := c.s3Client.GetObject(ctx, getInput)
if err != nil {
    return fmt.Errorf("unable to retrieve file: %w", err)
}
defer func() {
    if cerr := getOutput.Body.Close(); cerr != nil {
        log.Warn(fmt.Sprintf("failed to close S3 object body: %v", cerr))
    }
}()
```

For processes that might need cancellation, consider using context:

```go
ctx, cancel := context.WithCancel(context.Background())
defer cancel() // Ensure cancellation happens even on error paths

// Create command with context for lifecycle management
cmd := exec.CommandContext(ctx, cmdParts[0], cmdParts[1:]...)
```

This ensures all resources are properly cleaned up, error conditions during cleanup are logged, and long-running operations can be gracefully terminated.