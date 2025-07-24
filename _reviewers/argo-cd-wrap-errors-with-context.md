---
title: Wrap errors with context
description: When propagating errors up the call stack, always wrap them with contextual
  information about the failing operation using fmt.Errorf with the %w verb. This
  practice significantly improves debugging by providing a clear trail of what operations
  were being performed when the error occurred.
repository: argoproj/argo-cd
label: Error Handling
language: Go
comments_count: 8
repository_stars: 20149
---

When propagating errors up the call stack, always wrap them with contextual information about the failing operation using fmt.Errorf with the %w verb. This practice significantly improves debugging by providing a clear trail of what operations were being performed when the error occurred.

The pattern should be: `return fmt.Errorf("description of what failed: %w", err)`

Example from the codebase:
```go
// Instead of:
if err != nil {
    return err
}

// Do this:
if err != nil {
    return fmt.Errorf("failed to initialize oci client: %w", err)
}

// Or for more specific context:
objsMap, err := ctrl.getPermittedAppLiveObjects(destCluster, app, proj, projectClusters)
if err != nil {
    return fmt.Errorf("error getting permitted app live objects: %w", err)
}
```

This approach maintains the original error chain (allowing errors.Is and errors.As to work correctly) while adding valuable context about the operation that failed. It transforms generic errors into actionable debugging information, making it easier to identify the root cause and the sequence of operations that led to the failure.