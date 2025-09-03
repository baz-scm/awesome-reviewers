---
title: Follow naming patterns
description: 'Maintain consistent naming conventions throughout the codebase by following
  established patterns and avoiding redundancy. Key principles include:


  1. **Error naming**: Use the pattern `Err + [Subject] + [Error Condition]` (e.g.,
  `ErrStorageRetrievalFailed` instead of `ErrNotGetStorage`)'
repository: gofiber/fiber
label: Naming Conventions
language: Go
comments_count: 8
repository_stars: 37560
---

Maintain consistent naming conventions throughout the codebase by following established patterns and avoiding redundancy. Key principles include:

1. **Error naming**: Use the pattern `Err + [Subject] + [Error Condition]` (e.g., `ErrStorageRetrievalFailed` instead of `ErrNotGetStorage`)

2. **Test/benchmark naming**: Include underscores for consistency (`Test_` and `Benchmark_` prefixes)

3. **Constant naming**: Use descriptive names that indicate purpose (`DefaultFormat` instead of `FormatDefault`)

4. **Avoid redundant prefixes**: Don't repeat package context in type names (`KeyLookupFunc` instead of `KeyauthKeyLookupFunc`)

5. **Use proper English**: Avoid non-standard plurals or constructions (`AllFormData()` instead of `FormDatas()`)

6. **Function naming**: Choose concise, clear names that match existing patterns (`FromContext()` instead of `FromGoContext()`, `Logger()` to match similar functions)

Example of consistent error naming:
```go
// Good - follows Err + Subject + Condition pattern
ErrStorageRetrievalFailed = errors.New("unable to retrieve data from CSRF storage")
ErrStorageSaveFailed      = errors.New("unable to save data to CSRF storage")

// Avoid - inconsistent pattern
ErrNotGetStorage = errors.New("unable to retrieve data from CSRF storage")
```

This ensures code readability and helps developers quickly understand naming conventions when contributing to the project.