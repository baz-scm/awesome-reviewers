---
title: Deterministic DB Semantics
description: 'Make database changes (queries, migrations, and tests) explicit about
  shape and semantics: don’t rely on driver defaults, cached plan inference, or “looks
  right” reads when the DB can mask the truth.'
repository: maximhq/bifrost
label: Database
language: Go
comments_count: 7
repository_stars: 6862
---

Make database changes (queries, migrations, and tests) explicit about shape and semantics: don’t rely on driver defaults, cached plan inference, or “looks right” reads when the DB can mask the truth.

Apply this as a checklist:

1) Prove correctness with real row effects
- If the DB has read-time transforms/dedup (e.g., ClickHouse ReplacingMergeTree + FINAL), a “exists” style read can be misleading.
- Prefer assertions that measure the actual stored cardinality for the scenario you’re testing.

2) Migrations must use explicit projections and live-schema guards
- Avoid `SELECT *` inside migrations where earlier DDL in the same run can change column sets/types.
- Build an explicit projection from schema, then intersect with physically present/live columns to avoid selecting missing columns.
- Never depend on cached plans’ result types; keep queries previously-uncached by using a fixed explicit column list.

3) Index/DDL changes should be concurrency- and transaction-safe
- If an index needs `CONCURRENTLY`, create it outside transactional migration blocks (or via a post-startup mechanism) to avoid blocking/invalid transaction constraints.

4) Update paths must match the monotonic invariants
- Guard predicates must be carefully chosen for each statement’s boundary semantics (e.g., `<` vs `<=` depending on whether unchanged boundaries must still persist).
- If order matters within a transaction (flush overrides before advancing a “last_reset/last_*” boundary), encode it and ensure the guards remain valid.

5) Deterministic batching
- When batching with `LIMIT`, add an explicit `ORDER BY` so each batch removes the intended rows.
- If the driver reports unusable affected-row counts, compute the metric from a deterministic pre-selection (e.g., pluck ids, then delete).

Example (deterministic batch delete with correct counting):
```go
func (s *ClickHouseLogStore) DeleteLogsBatch(ctx context.Context, cutoff time.Time, batchSize int) (int64, error) {
  var ids []string
  if err := s.db.WithContext(ctx).
    Model(&Log{}).
    Select("id").
    Where("created_at < ?", cutoff).
    Order("created_at ASC").
    Limit(batchSize).
    Pluck("id", &ids).Error; err != nil {
    return 0, err
  }

  res := s.db.WithContext(ctx).Where("id IN (?)", ids).Delete(&Log{})
  _ = res // affected rows may be driver-rewritten; rely on len(ids)
  return int64(len(ids)), res.Error
}
```

Outcome: DB code and migrations become robust to schema drift, driver quirks, and boundary/dedup semantics—so correctness is both provable and repeatable across environments.