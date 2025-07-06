---
title: Names should be descriptive
description: Use clear, descriptive names while avoiding redundant qualifiers. Choose
  full words over abbreviations unless the abbreviated form is widely recognized.
  When a type or context already implies certain qualities, avoid repeating them in
  the name.
repository: astral-sh/uv
label: Naming Conventions
language: Rust
comments_count: 8
repository_stars: 60322
---

Use clear, descriptive names while avoiding redundant qualifiers. Choose full words over abbreviations unless the abbreviated form is widely recognized. When a type or context already implies certain qualities, avoid repeating them in the name.

Good examples:
```rust
// Good: Clear, descriptive names
let preferred = if cfg!(all(windows, target_arch = "aarch64")) { ... }
fn find_pyvenv_cfg_version_conflict(&self) -> Option<(Version, Version)> { ... }

// Bad: Unnecessary qualifiers, abbreviations
let maybe_index_url: Option<&Url> = ...  // Use just 'index_url' - Option implies maybe
let auth_indexes: AuthIndexes = ...      // Use just 'indexes' in auth context
let tool_py_req = ...                    // Use 'tool_python_request' instead
```

Maintain naming consistency with existing codebase patterns. If a particular name is used consistently throughout the codebase (e.g., 's' for pluralization), follow that convention unless there's a compelling reason to change it.