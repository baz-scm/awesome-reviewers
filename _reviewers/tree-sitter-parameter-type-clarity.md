---
title: parameter type clarity
description: Design API parameters using specific, intention-revealing types rather
  than generic or ambiguous ones. This improves code readability, prevents misuse,
  and makes the API's behavior self-documenting.
repository: tree-sitter/tree-sitter
label: API
language: Rust
comments_count: 4
repository_stars: 21799
---

Design API parameters using specific, intention-revealing types rather than generic or ambiguous ones. This improves code readability, prevents misuse, and makes the API's behavior self-documenting.

Key principles:
- Use `Option<T>` instead of default values when a parameter is truly optional
- Replace multiple related boolean flags with a single enum parameter
- Prefer specific parameter types over generic ones when the function has focused responsibilities

Examples of improvements:

**Replace default values with Option when appropriate:**
```rust
// Before: Unclear if version is required
struct Version {
    #[arg(default_value = "0.0.0")]
    pub version: SemverVersion,
}

// After: Clear that version is optional
struct Version {
    pub version: Option<SemverVersion>,
}
```

**Replace multiple bools with enum:**
```rust
// Before: Multiple related flags
pub bump: bool,
pub bump_minor: bool, 
pub bump_major: bool,

// After: Single enum parameter
pub bump: Option<BumpType>, // where BumpType = { Patch, Minor, Major }
```

**Use specific parameters over generic ones:**
```rust
// Before: Generic but unclear
fn needs_recompile(lib_path: &Path, parser_c_path: &Path, scanner_path: &Option<PathBuf>, external_files_paths: &[PathBuf])

// After: Generalized and clear
fn needs_recompile(checking_paths: &[Path])
```

This approach makes function signatures self-documenting and reduces the cognitive load on API consumers by making valid usage patterns explicit in the type system.