---
title: Minimize API scope
description: When designing APIs, prioritize simplicity and focused scope over feature
  completeness. Before adding new API methods or expanding existing ones, evaluate
  whether the functionality can be achieved with existing interfaces. APIs that spread
  across multiple modules or introduce complex signatures often indicate scope creep
  that should be avoided.
repository: jj-vcs/jj
label: API
language: Markdown
comments_count: 4
repository_stars: 21171
---

When designing APIs, prioritize simplicity and focused scope over feature completeness. Before adding new API methods or expanding existing ones, evaluate whether the functionality can be achieved with existing interfaces. APIs that spread across multiple modules or introduce complex signatures often indicate scope creep that should be avoided.

Key principles:
- Question necessity: Ask "can this be achieved with existing APIs?" before adding new ones
- Limit cross-module impact: Prefer keeping functionality contained within single modules when possible  
- Simplify signatures: Avoid overly complex method signatures that take multiple generic parameters or require deep domain knowledge

For example, instead of adding a new `ext:` fileset operator when `glob:"**/*.rs"` already works, consider whether the convenience justifies the additional API surface. Similarly, when an API signature becomes complex like:

```rust
pub fn search(
    &self,
    path: &RepoPath,
    attribute_names: impl AsRef<[&str]>,
    priority: SearchPriority,
) -> Result<HashMap<String, gix_attributes::State>>
```

Consider simpler alternatives that drop unnecessary parameters or use more focused types:

```rust
pub fn search(
   &self,
   path: &RepoPath, 
   attribute_names: &[&str]
) -> Result<...>
```

This approach prevents APIs from becoming unwieldy and reduces maintenance burden while keeping the codebase more approachable for contributors.