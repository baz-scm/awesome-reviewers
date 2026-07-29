---
title: Migration consistency rules
description: 'When changing config schemas, treat migrations as part of the API contract:
  migrations must be safe under partial/legacy states and must not cause read/write
  skew that overwrites migrated data.'
repository: aaif-goose/goose
label: Migrations
language: Rust
comments_count: 5
repository_stars: 51876
---

When changing config schemas, treat migrations as part of the API contract: migrations must be safe under partial/legacy states and must not cause read/write skew that overwrites migrated data.

Practical standard:
1) Backfill before cleanup: if legacy keys are being removed while the new structured block exists, first reconstruct any missing new keys needed to preserve user intent (e.g., `active_provider`), then delete legacy keys.
2) Prevent clobbering across read vs write: ensure the code path that *reads* values used to construct a write payload sees the same logical (post-migration) state, or explicitly preserve fields that the migration may have created.
3) Use runtime guards for legacy placeholders: if old entries used sentinel values, detect them during lookup/migration and correct behavior without requiring disk rewrites.
4) Split migrations by side effects, but keep behavior consistent: if `load()` intentionally does not persist provider migrations, then any logic that constructs persisted updates must account for that (e.g., preserve active provider fields after migration).

Example pattern for (2): preserve the migrated model only when updating the active provider; otherwise write a new empty/default model.

```rust
let model = if goose::config::get_active_provider(config)
    .as_deref()
    == Some(provider_name.as_str())
{
    config.get_goose_model().unwrap_or_default() // preserved for active provider
} else {
    String::new() // new provider
};

goose::config::set_provider_entry(
    config,
    &provider_name,
    &goose::config::ProviderEntry {
        enabled: true,
        model,
        configured: true,
    },
)?;
```

Apply this style whenever a migration changes where authoritative fields live (flat keys → structured blocks, sentinel fixes, etc.).