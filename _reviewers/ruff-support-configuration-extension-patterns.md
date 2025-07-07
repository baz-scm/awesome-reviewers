---
title: Support configuration extension patterns
description: When designing configuration systems, provide both replacement and extension
  options for list-based settings to give users flexibility in how they modify default
  configurations.
repository: astral-sh/ruff
label: Configurations
language: Rust
comments_count: 4
repository_stars: 40619
---

When designing configuration systems, provide both replacement and extension options for list-based settings to give users flexibility in how they modify default configurations.

For list-based configurations, consider implementing:
1. A base option for complete replacement (`allow_abc_meta_bases`)
2. An extension option that appends to defaults (`extend_abc_meta_bases`)

This approach allows users to either:
- Override the entire list when they need complete control
- Add to the existing defaults when they only need minor adjustments

```rust
#[option(
    default = r#"["typing.Protocol", "typing_extensions.Protocol"]"#,
    value_type = "list[str]",
    example = r#"allow-abc-meta-bases = ["my_package.SpecialBaseClass"]"#
)]
pub allow_abc_meta_bases: Vec<String>,

#[option(
    default = r#"[]"#,
    value_type = "list[str]", 
    example = r#"extend-abc-meta-bases = ["my_package.SpecialBaseClass"]"#
)]
pub extend_abc_meta_bases: Vec<String>,
```

When implementing the options, combine them at the settings level rather than requiring consumers to check both settings:

```rust
// In your settings structure
pub struct Settings {
    // Combined at initialization time
    pub allowed_bases: FxHashSet<String>,
}

// When constructing settings
let mut allowed_bases = options.allow_abc_meta_bases.into_iter().collect::<FxHashSet<_>>();
allowed_bases.extend(options.extend_abc_meta_bases.iter().cloned());
```

This pattern promotes cleaner code that consumes the settings, making it less error-prone and easier to maintain.