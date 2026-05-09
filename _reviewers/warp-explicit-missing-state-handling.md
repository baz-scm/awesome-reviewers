---
title: Explicit Missing-State Handling
description: When data is optional/unknown, handle it intentionally and explicitly—either
  skip the feature (return `None`) or fall back to a safe default—never via implicit
  drop or placeholder sentinel values.
repository: warpdotdev/warp
label: Null Handling
language: Rust
comments_count: 6
repository_stars: 56893
---

When data is optional/unknown, handle it intentionally and explicitly—either skip the feature (return `None`) or fall back to a safe default—never via implicit drop or placeholder sentinel values.

Standards:
1) Use `Option` (or “unset” fields) to represent missingness. Don’t encode “missing user” as an empty string; use `Option<String>` (or clear the field) instead.
2) For optional features: return `None` when the input is absent or invalid (e.g., empty/unparseable config) so you don’t inject placeholder context.
3) For UX that must keep working: when an identifier can’t be resolved (unknown profile/name), fall back to a defined default rather than aborting.
4) Enforce invariants in types: if `None` should never occur, remove `Option` from parameters/fields and make it impossible to construct invalid states.
5) Be explicit in branching: enumerate all enum/location/type cases so non-local/null/unknown cases don’t get silently mishandled.

Example pattern (skip-or-fallback):
```rust
fn resolve_profile(agent_profile_name: Option<&str>, default_profile: &str) -> Option<&str> {
    match agent_profile_name {
        None => Some(default_profile),
        Some(name) if is_known_profile(name) => Some(name),
        Some(_unknown) => {
            // Unknown should still resolve to something usable.
            Some(default_profile)
        }
    }
}

fn load_optional_context(path: &Path) -> Option<String> {
    let content = path.read_to_string().ok()?; // absent/IO error => None
    if content.trim().is_empty() {
        return None; // invalid/empty config => None (don’t inject placeholders)
    }
    Some(content)
}
```