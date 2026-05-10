---
title: Preserve Backward Compatibility
description: When making schema/proto changes, never remove (or repurpose) legacy
  layer parameters that existing models/configs rely on. For backward compatibility
  migrations, keep the old message/field definitions, mark them deprecated if appropriate,
  and implement translation/mapping to the new schema rather than dropping support.
repository: Tencent/ncnn
label: Migrations
language: Other
comments_count: 2
repository_stars: 23205
---

When making schema/proto changes, never remove (or repurpose) legacy layer parameters that existing models/configs rely on. For backward compatibility migrations, keep the old message/field definitions, mark them deprecated if appropriate, and implement translation/mapping to the new schema rather than dropping support.

Guideline (Proto example):
- If you need to evolve `LayerParameter`, add new optional fields with new tag numbers.
- Do **not** delete existing BN parameter fields/messages used by older serialized configs.
- If you must change behavior, keep the old schema elements and route them to the new implementation.

Example pattern:
```proto
message LayerParameter {
  // Legacy BN parameters must remain for old configs
  optional BNParameter bn_param = 45; // keep, don’t remove

  // New parameters added safely with new field numbers
  optional AnnotatedDataParameter annotated_data_param = 200;

  // If migrating semantics, keep BNParameter but implement conversion in code.
}

// Keep BNParameter definition for compatibility; optionally mark as deprecated.
message BNParameter {
  optional FillerParameter filler = 3;
}
```
Also add a migration/compatibility test: load an older BN-containing config/model and verify it still parses and runs.