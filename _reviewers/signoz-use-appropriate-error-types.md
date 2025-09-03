---
title: Use appropriate error types
description: Always use semantically correct error types and codes that match the
  actual failure scenario. This ensures proper error handling by callers and consistent
  API behavior across the system.
repository: SigNoz/signoz
label: Error Handling
language: Go
comments_count: 5
repository_stars: 23369
---

Always use semantically correct error types and codes that match the actual failure scenario. This ensures proper error handling by callers and consistent API behavior across the system.

**Key Guidelines:**
- Use `TypeNotFound`/`CodeNotFound` for missing resources, not `TypeInternal`/`CodeInternal`
- Use `TypeInvalidInput`/`CodeInvalidInput` for validation failures, not `TypeForbidden`/`CodeForbidden`
- Always check for errors, even in operations you expect to succeed
- Return proper errors instead of nil/empty results when operations fail

**Examples:**

❌ **Incorrect - Wrong error type for not found:**
```go
return nil, s.sqlstore.WrapNotFoundErrf(err, errors.CodeInternal, "unable to fetch the license with ID: %s", licenseID)
```

✅ **Correct - Proper not found error:**
```go
return nil, s.sqlstore.WrapNotFoundErrf(err, errors.CodeNotFound, "unable to fetch the license with ID: %s", licenseID)
```

❌ **Incorrect - Wrong error type for validation:**
```go
return errors.Wrapf(nil, errors.TypeForbidden, errors.CodeForbidden, "s3 buckets can only be added to service-type[%s]", services.S3Sync)
```

✅ **Correct - Proper validation error:**
```go
return errors.Newf(errors.TypeInvalidInput, errors.CodeInvalidInput, "s3 buckets can only be added to service-type[%s]", services.S3Sync)
```

❌ **Incorrect - Missing error check:**
```go
tracesJSON, _ := json.Marshal(tracesFilters)
```

✅ **Correct - Always check errors:**
```go
tracesJSON, err := json.Marshal(tracesFilters)
if err != nil {
    return nil, err
}
```

This practice ensures that error handling is predictable and allows callers to make appropriate decisions based on the specific type of failure.