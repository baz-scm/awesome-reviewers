---
title: wrap errors properly
description: When creating error messages that include information from underlying
  errors, use fmt.Errorf with the %w verb instead of string concatenation with err.Error().
  This preserves the error chain, enabling proper error unwrapping and better debugging
  capabilities.
repository: golang/go
label: Error Handling
language: Go
comments_count: 2
repository_stars: 129599
---

When creating error messages that include information from underlying errors, use fmt.Errorf with the %w verb instead of string concatenation with err.Error(). This preserves the error chain, enabling proper error unwrapping and better debugging capabilities.

String concatenation breaks the error chain and prevents tools and code from accessing the original error:
```go
// Bad: breaks error chain
return nil, errors.New("x509: failed to serialize extensions attribute: " + err.Error())

// Good: preserves error chain
return nil, fmt.Errorf("x509: failed to serialize extensions attribute: %w", err)
```

The wrapped error can then be unwrapped using errors.Unwrap() or checked with errors.Is() and errors.As(). Consider documenting when your functions return errors that implement Unwrap() []error method to make the unwrapping behavior explicit to callers.