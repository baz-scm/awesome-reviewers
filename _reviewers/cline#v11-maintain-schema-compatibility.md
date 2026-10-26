---
title: Maintain Schema Compatibility
description: When an API contract is defined via generated schema files (e.g., protobuf),
  update it by changing the source-of-truth and regenerating—then verify with build/type
  checks. If you deprecate or remove values from the public API contract (especially
  enums), explicitly reserve those values/names so they can’t be reused and compatibility
  expectations aren’t...
repository: cline/cline#v11
label: API
language: Other
comments_count: 2
repository_stars: 70871
---

When an API contract is defined via generated schema files (e.g., protobuf), update it by changing the source-of-truth and regenerating—then verify with build/type checks. If you deprecate or remove values from the public API contract (especially enums), explicitly reserve those values/names so they can’t be reused and compatibility expectations aren’t broken.

Apply this as a standard for API/schema changes:
- **Schema updates**: edit the generator’s source (not the generated `.proto` directly), then run the generator and confirm the output matches (no unexpected git diff) and passes validation.
- **Enum/value removals**: add `reserved` entries for removed enum numbers and/or names.

Example (protobuf enum compatibility):
```proto
enum ClineAsk {
  USE_MCP_SERVER = 11;
  NEW_TASK = 12;
  CONDENSE = 13;

  // REPORT_BUG removed; keep the value reserved for compatibility
  reserved 14;
  reserved "REPORT_BUG";

  SUMMARIZE_TASK = 15;
}
```

Example (regenerate + verify workflow):
```sh
node scripts/generate-state-proto.mjs
npm run protos
npm run check-types
```