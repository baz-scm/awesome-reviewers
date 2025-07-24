---
title: Comprehensive function documentation
description: 'Functions should have thorough documentation that follows Go conventions
  and explains both the "what" and "why" of the code. This includes:


  1. **Proper Go doc format**: Start function comments with the function name, e.g.,
  "GetSecretByName returns the Secret..." instead of "Returns the Secret..."'
repository: argoproj/argo-cd
label: Documentation
language: Go
comments_count: 3
repository_stars: 20149
---

Functions should have thorough documentation that follows Go conventions and explains both the "what" and "why" of the code. This includes:

1. **Proper Go doc format**: Start function comments with the function name, e.g., "GetSecretByName returns the Secret..." instead of "Returns the Secret..."

2. **Explain complex logic**: Add explanatory comments for non-obvious code sections that describe why the logic exists, not just what it does.

3. **Document all parameters and return values**: Provide clear descriptions of what each parameter represents and what the function returns, especially for complex functions with multiple return values.

4. **Include context and intent**: Explain the purpose and use cases of the function, particularly for complex business logic.

Example of good documentation:
```go
// alreadyAttemptedSync is meant to help the caller understand whether an identical sync operation 
// has been attempted, to avoid excessively retrying the exact same sync operation.
//
// alreadyAttemptedSync returns true if either 1) newRevisionHasChanges is true and the most recently 
// synced revision(s) exactly match the given desiredRevisions, 2) newRevisionHasChanges is false and 
// the most recently synced app source configuration matches exactly the current app source configuration, 
// or 3) the most recent operation state is missing a sync result but the sync phase is completed.
//
// TODO: remove the last two return parameters, since they're effectively just aliases for fields 
// on the app object.
func alreadyAttemptedSync(app *appv1.Application, desiredRevisions []string, newRevisionHasChanges bool) (bool, []string, synccommon.OperationPhase) {
    // If pruning is enabled and the app is *not* allowed to have an empty desired state,
    // we need to ensure we're not about to accidentally wipe out all resources.
    // This is a safety mechanism to prevent full deletion due to automation errors (e.g., empty Git path).
    if app.Spec.SyncPolicy.Automated.Prune && !app.Spec.SyncPolicy.Automated.AllowEmpty {
        // ... implementation
    }
}
```

Well-documented code reduces cognitive load for reviewers and future maintainers, making the codebase more accessible and maintainable.