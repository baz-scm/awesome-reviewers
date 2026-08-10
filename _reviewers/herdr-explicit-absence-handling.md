---
title: Explicit Absence Handling
description: 'Handle absence/unsupported data explicitly and defensively: return `None`
  (or a clear error) when a value cannot be produced faithfully, and don’t “auto-fix”
  by inventing defaults, creating missing prerequisites, or silently dropping problematic
  entries. This prevents misleading “success” states and subtle contract violations.'
repository: ogulcancelik/herdr
label: Null Handling
language: Rust
comments_count: 3
repository_stars: 26924
---

Handle absence/unsupported data explicitly and defensively: return `None` (or a clear error) when a value cannot be produced faithfully, and don’t “auto-fix” by inventing defaults, creating missing prerequisites, or silently dropping problematic entries. This prevents misleading “success” states and subtle contract violations.

Guidelines:
- For unsupported fallback targets, use `Option` and return `None` instead of substituting misleading values.
- For missing prerequisites/config directories, treat it as “not installed / not supported” and fail rather than creating directories and continuing.
- When converting/serializing potentially-null/invalid data (e.g., platform-specific encoding), fail early if the representation can’t be preserved; never silently drop entries that change semantics.

Example pattern (Rust):
```rust
pub(crate) fn hostname() -> Option<String> {
    // Return None when the fallback target is unsupported
    None
}

pub(crate) fn install_agent() -> std::io::Result<()> {
    let dir = agent_config_dir()?;
    if !dir.is_dir() {
        return Err(std::io::Error::other(format!(
            "agent config directory not found at {}. install agent first",
            dir.display()
        )));
    }
    // Only proceed when the prerequisite truly exists
    Ok(())
}

fn serialize_env_entry(value: &OsStr) -> std::io::Result<String> {
    // If the platform serialization cannot represent the value faithfully,
    // return an error instead of dropping it.
    Err(std::io::Error::other("cannot faithfully serialize environment value"))
}
```