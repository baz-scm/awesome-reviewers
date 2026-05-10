---
title: Version Compatibility First
description: 'When changing serialized/wire formats (RDB/DUMP/RESTORE or module metadata),
  treat it as a data migration: define compatibility behavior and make encoding placement
  deterministic.'
repository: redis/redis
label: Migrations
language: Other
comments_count: 3
repository_stars: 74261
---

When changing serialized/wire formats (RDB/DUMP/RESTORE or module metadata), treat it as a data migration: define compatibility behavior and make encoding placement deterministic.

Apply these rules:
1) Version/format contract: if new RDB object types or metadata layouts are introduced, explicitly decide whether you will (a) bump the RDB/module format version, or (b) keep old encodings unchanged unless the new feature is used. Ensure the code and release process agree on the final version.
2) Upgrade/downgrade story: document what happens when a newer producer writes data that an older consumer might load/replicate. If the new encoding can appear only under certain runtime conditions (e.g., “only when XNACK was used”), spell out the exact condition and the resulting failure mode.
3) Deterministic metadata placement: avoid “lazy first occurrence” schemes that produce structurally different files depending on which keys appear first.
   - Prefer writing global metadata/class definitions at a deterministic location (e.g., beginning of the RDB/DUMP), or
   - Prefer embedding complete metadata context per key as an atomic unit (e.g., `<META, TYPE, KEY, VALUE>`), so partial loading/streaming doesn’t require global state.
4) Don’t rely on “compat isn’t important”: even if you plan a version bump, compatibility impacts replication and user workflows; decide and implement the intended behavior deliberately.

Illustrative pattern (eager header vs per-key embedding):
```c
// Option A: eager, deterministic header (fixed location)
write_rdb_header();
write_meta_class_definitions();
for (each key) {
    write_key_with_value_without_global_state();
}

// Option B: per-key atomic embedding (metadata always complete)
for (each key) {
    write(T_META);
    write(TYPE);
    write(KEY);
    write(VALUE);
}
```