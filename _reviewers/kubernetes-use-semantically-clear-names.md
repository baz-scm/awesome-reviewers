---
title: Use semantically clear names
description: Choose names that accurately reflect the actual functionality, purpose,
  or semantic meaning rather than using generic, misleading, or implementation-focused
  terms. Names should be self-documenting and help readers understand what the code
  does without needing additional context.
repository: kubernetes/kubernetes
label: Naming Conventions
language: Go
comments_count: 11
repository_stars: 116489
---

Choose names that accurately reflect the actual functionality, purpose, or semantic meaning rather than using generic, misleading, or implementation-focused terms. Names should be self-documenting and help readers understand what the code does without needing additional context.

**Key principles:**
- **Reflect actual purpose**: Function names should describe what they actually do, not just part of their implementation
- **Avoid misleading implications**: Field names should not suggest behavior they don't have (e.g., "Minimum" implying "at least" when it means "exact amount")  
- **Be specific over generic**: Use descriptive names instead of vague suffixes like "Extended" or "Helper"
- **Match semantic meaning**: Variable names should reflect their role in the business logic

**Examples:**

```go
// Bad: Generic and doesn't explain what it does
func initialize() error

// Good: Describes the actual purpose  
func migrateRecordVersions() error

// Bad: Misleading - suggests "at least" semantics
type CapacityRequirements struct {
    Minimum map[QualifiedName]resource.Quantity
}

// Good: Clear about guaranteed allocation
type CapacityRequirements struct {
    Requests map[QualifiedName]resource.Quantity  
}

// Bad: Generic variable name
bound, err := isClaimReadyForBinding(claim)

// Good: Semantic meaning is clear
ready, err := isClaimReadyForBinding(claim)

// Bad: Overloaded term "binding" used imprecisely  
func isClaimBound(claim *ResourceClaim) bool

// Good: Precise about what condition is being checked
func isClaimReadyForBinding(claim *ResourceClaim) bool
```

This approach improves code readability and reduces the cognitive load on developers trying to understand the codebase.