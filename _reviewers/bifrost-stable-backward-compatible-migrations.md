---
title: Stable Backward-Compatible Migrations
description: 'When adding schema/config fields, design migrations to be stable across
  upgrade/downgrade boundaries:


  - Handle “unset vs default” explicitly in config-store: store a sentinel/unset value
  (commonly `0`), ensure getters apply the real default (e.g., 15), and ensure config
  hashing only incorporates the field when it is explicitly set (non-zero). Add a
  test...'
repository: maximhq/bifrost
label: Migrations
language: Go
comments_count: 5
repository_stars: 6862
---

When adding schema/config fields, design migrations to be stable across upgrade/downgrade boundaries:

- Handle “unset vs default” explicitly in config-store: store a sentinel/unset value (commonly `0`), ensure getters apply the real default (e.g., 15), and ensure config hashing only incorporates the field when it is explicitly set (non-zero). Add a test that proves no config churn for unset values.
- Use consistent migration patterns:
  - Prefer helper patterns like `addColumnIfNotExists` / `dropColumnIfExists` and the repo’s column existence checks.
  - Decide rollback policy based on intent:
    - Additive-only schema changes (adding new columns, no data move/transform) should be reversible (rollback drops only the added columns).
    - If a migration transforms/moves existing data (or intentionally relies on older binaries ignoring new columns), don’t pretend rollback can restore prior state—mark it non-rollbackable per existing precedent.

Example pattern for config hash stability (Go):
```go
// In GenerateClientConfigHash
if streamKeepAliveInterval != 0 { // only fold explicit values
    h.WriteString(fmt.Sprintf("stream_keepalive_interval=%d", streamKeepAliveInterval))
}

// In getter (or load/default layer)
if storedInterval == 0 {
    return 15 // default
}
```

Example pattern for reversible additive migrations:
```go
Migrate: func(tx *gorm.DB) error {
    return addColumnIfNotExists(tx, logger, &tables.TableKey{}, "bedrock_project_id")
},
Rollback: func(tx *gorm.DB) error {
    return dropColumnIfExists(tx, logger, &tables.TableKey{}, "bedrock_project_id")
},
```

Apply this standard anytime you change config-store schema, add new columns used by runtime behavior, or touch migration rollback behavior—aim for upgrades that don’t break existing rows or cause unintended hash/config regeneration, while keeping rollback aligned with what the migration actually changes.