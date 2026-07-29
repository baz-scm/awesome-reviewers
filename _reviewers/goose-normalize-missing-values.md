---
title: Normalize Missing Values
description: 'When handling optional/missing inputs, **normalize and guard early**
  so “missing” can’t accidentally become a real value or clobber existing state.


  Rules:'
repository: aaif-goose/goose
label: Null Handling
language: Rust
comments_count: 6
repository_stars: 51876
---

When handling optional/missing inputs, **normalize and guard early** so “missing” can’t accidentally become a real value or clobber existing state.

Rules:
1. **Normalize sentinels to `None` immediately** (e.g., treat `Some(0)`/`""`/placeholder numbers as “unset”), before applying fallback chains or “is set?” logic.
2. **Gate behavior on prerequisites**: if a required resource/path value is missing, return a structured error or defer activation—do not proceed with a potentially wrong default.
3. **Preserve on partial updates/imports**: only overwrite fields that were actually provided; never default missing fields to empty values.
4. **Choose semantics for “missing vs explicit off”**: omission vs sending an explicit value should be deliberate and tested against downstream behavior.

Example (Rust):
```rust
fn apply_update(existing: &mut Config, input: &Input) -> anyhow::Result<()> {
    // 1) Normalize “not configured” sentinel -> None
    let new_limit: Option<usize> = match input.context_limit {
        Some(0) | None => None,
        Some(v) => Some(v),
    };

    // 2) Preserve unspecified fields (partial update)
    if let Some(limit) = new_limit {
        existing.context_limit = Some(limit);
    }

    if let Some(new_provider) = input.provider.as_deref() {
        if !new_provider.is_empty() {
            existing.provider = new_provider.to_string();
        }
    }

    // 3) Guard on prerequisites (defer/return)
    if existing.working_dir_missing() {
        anyhow::bail!("working_dir_missing");
    }

    Ok(())
}
```
Use this pattern consistently across null/optional fields, sentinels, and partial request bodies to avoid meaning drift and state poisoning.