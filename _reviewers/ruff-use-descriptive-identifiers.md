---
title: Use descriptive identifiers
description: Avoid abbreviations in variable, parameter, and method names to improve
  code readability and maintainability. Use descriptive identifiers that clearly indicate
  the purpose and content of what they represent.
repository: astral-sh/ruff
label: Naming Conventions
language: Rust
comments_count: 5
repository_stars: 40619
---

Avoid abbreviations in variable, parameter, and method names to improve code readability and maintainability. Use descriptive identifiers that clearly indicate the purpose and content of what they represent.

Instead of:
```rust
// Abbreviated variable names
let spec = self.specialization;
let ctx = self.generic_context;
let ty = self.inferred_return_type();
let tvar = TypeVar(...);
```

Prefer:
```rust
// Descriptive variable names
let specialization = self.specialization;
let generic_context = self.generic_context;
let return_type = self.inferred_return_type();
let type_var = TypeVar(...);
```

Additionally:
- Functions should use verb phrases: use `infer_return_type()` not `inferred_return_ty()`
- Use meaningful variable names that match what they represent: if a variable holds a place expression, name it `place_expr` not just `expr`
- For generated/synthetic names (like type variables), use distinctive names that won't conflict with common user code: use `T_all` instead of just `T`
- Choose names that reflect the semantic meaning of the data, not just its type

Descriptive names make code easier to understand at first glance and reduce the cognitive load required to comprehend complex logic.