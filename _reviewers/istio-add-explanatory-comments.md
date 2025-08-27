---
title: Add explanatory comments
description: 'Code should include explanatory comments that help future maintainers
  understand complex logic, design decisions, field semantics, and non-obvious implementation
  details. Comments are especially important for:'
repository: istio/istio
label: Documentation
language: Go
comments_count: 9
repository_stars: 37192
---

Code should include explanatory comments that help future maintainers understand complex logic, design decisions, field semantics, and non-obvious implementation details. Comments are especially important for:

- Complex algorithms and business logic that aren't immediately clear from the code
- Field semantics, constraints, and expected behavior when dealing with collections or modified data structures
- Design decisions and rationale, particularly when multiple approaches were possible
- Magic numbers, constants, and hardcoded values
- External references like KEPs, RFCs, or documentation that provide context

Comments should follow Go conventions by being placed above the code they describe rather than inline, and should be detailed enough to explain both the "what" and "why" of the implementation.

Example of good explanatory commenting:
```go
// WithServices marks multiple services as part of the selection criteria. This is used when we want to find **all** policies attached to a specific proxy instance, rather than scoped to a specific service. This is useful when using ECDS, for example, where we might have:
// * Each unique service creates a listener, and applies a policy selected by `WithService` pointing to ECDS  
// * All policies are found, by `WithServices`, and returned in ECDS
func (p WorkloadPolicyMatcher) WithServices(services []*Service) WorkloadPolicyMatcher {
    // implementation...
}

// Addresses contains the endpoint addresses. All elements must have the same metadata
// and represent the same logical endpoint across different network interfaces.
Addresses []string
```

This practice significantly improves code maintainability and reduces the cognitive load for developers working with unfamiliar codebases.