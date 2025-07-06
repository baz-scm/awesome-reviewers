---
title: Choose domain-specific semantic names
description: 'Names should clearly reflect their domain-specific meaning and purpose,
  avoiding generic or ambiguous terms. This applies to variables, methods, classes,
  and other identifiers. When naming, consider:'
repository: zed-industries/zed
label: Naming Conventions
language: Rust
comments_count: 5
repository_stars: 62119
---

Names should clearly reflect their domain-specific meaning and purpose, avoiding generic or ambiguous terms. This applies to variables, methods, classes, and other identifiers. When naming, consider:

1. Use domain terminology that precisely describes the concept
2. Avoid broad or generic terms that could be ambiguous in the codebase context
3. Be explicit about the purpose or behavior
4. Maintain consistency with established domain naming patterns

Example:
```rust
// Avoid: Generic or ambiguous names
pub fn tokens(&self) -> &Arc<SemanticTheme> { ... }
let askpass_content = format!(...);

// Better: Domain-specific semantic names
pub fn semantic_tokens(&self) -> &Arc<SemanticTheme> { ... }
let askpass_script = format!(...);
```

This approach helps maintain clarity and reduces confusion, especially in large codebases where context may not be immediately apparent. When introducing new names, ensure they align with the domain language used throughout the project.