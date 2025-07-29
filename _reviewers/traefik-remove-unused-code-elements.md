---
title: Remove unused code elements
description: Eliminate unnecessary code elements including unused parameters, struct
  tags, methods, and dead code to improve code cleanliness and maintainability. Unused
  code creates confusion for maintainers and adds unnecessary complexity to the codebase.
repository: traefik/traefik
label: Code Style
language: Go
comments_count: 3
repository_stars: 55772
---

Eliminate unnecessary code elements including unused parameters, struct tags, methods, and dead code to improve code cleanliness and maintainability. Unused code creates confusion for maintainers and adds unnecessary complexity to the codebase.

Key areas to review:
- Remove unused function parameters that serve no purpose
- Delete unnecessary struct tags that aren't used in the current context
- Remove unused methods and functions that have no callers
- Clean up dead code that serves no functional purpose

Example of unused parameter removal:
```go
// Before: req parameter is unused
func (b *BasicLimiter) Allow(ctx context.Context, source string, amount int64, req *http.Request, rw http.ResponseWriter) {
    // req is never used, only ctx is needed
}

// After: remove unused parameter
func (b *BasicLimiter) Allow(ctx context.Context, source string, amount int64, rw http.ResponseWriter) {
    // cleaner function signature
}
```

Example of unnecessary struct tag removal:
```go
// Before: description tag not needed in dynamic config
type Redis struct {
    Endpoints []string `description:"KV store endpoints." json:"endpoints,omitempty"`
}

// After: remove unused description tag
type Redis struct {
    Endpoints []string `json:"endpoints,omitempty"`
}
```

Regularly audit code for unused elements during code reviews to maintain a clean, maintainable codebase.