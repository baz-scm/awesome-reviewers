---
title: Domain-specific error boundaries
description: Define and use domain-specific error types within bounded contexts rather
  than relying on generic service errors. Each component/package should define its
  own error types that reflect its domain concepts, avoiding dependencies on external
  error frameworks.
repository: temporalio/temporal
label: Error Handling
language: Go
comments_count: 5
repository_stars: 14953
---

Define and use domain-specific error types within bounded contexts rather than relying on generic service errors. Each component/package should define its own error types that reflect its domain concepts, avoiding dependencies on external error frameworks.

Key points:
1. Define custom error types for your domain/component
2. Avoid using service-level errors (e.g. gRPC errors) in application code
3. Convert between error types at system boundaries
4. Include relevant context in error messages

Example:
```go
// Bad - using service errors in application code
func (n *Node) validateCollection(field string) error {
    if field.val.Kind() != reflect.Map {
        return serviceerror.NewInternal("invalid collection type")
    }
    return nil
}

// Good - using domain-specific errors
type ValidationError struct {
    Field string
    Reason string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed for %s: %s", e.Field, e.Reason)
}

func (n *Node) validateCollection(field string) error {
    if field.val.Kind() != reflect.Map {
        return &ValidationError{
            Field: field,
            Reason: "must be a map type",
        }
    }
    return nil
}

// Convert domain errors to service errors at system boundaries
func (s *Service) handleRequest() error {
    err := domain.Operation()
    if err != nil {
        // Convert domain errors to appropriate service errors
        var valErr *ValidationError
        if errors.As(err, &valErr) {
            return serviceerror.NewInvalidArgument(valErr.Error())
        }
        return serviceerror.NewInternal("unexpected error")
    }
    return nil
}
```