---
title: Backward-Compatible Proto Migrations
description: 'When migrating protobuf schemas, make changes deterministic and backward
  compatible:


  1) Treat generated proto files as outputs of a single source of truth.'
repository: cline/cline#v28
label: Migrations
language: Other
comments_count: 2
repository_stars: 70893
---

When migrating protobuf schemas, make changes deterministic and backward compatible:

1) Treat generated proto files as outputs of a single source of truth.
- After editing the generator inputs (e.g., state-keys / config), rerun the generator and the repo’s proto/type validation (e.g., `npm run protos` / `npm run check-types`).
- Ensure the generated files produce the expected field updates and do not introduce accidental diffs.

2) Preserve compatibility when removing enum values.
- Don’t delete an enum entry without reserving the old tag and name to prevent reuse and to document the removal.

Example (enum removal compatibility):
```proto
enum ClineAsk {
  USE_MCP_SERVER = 11;
  NEW_TASK = 12;
  CONDENSE = 13;

  reserved 14;            // REPORT_BUG (removed)
  reserved "REPORT_BUG";

  SUMMARIZE_TASK = 15;
}
```

3) Merge only after the migration is validated.
- Regenerate/protos-check, and confirm type checks pass so the migration is consistent across all generated artifacts and consumers.