---
title: Backcompatible Migration Contract
description: 'When making schema/connector changes that can affect existing customer
  deployments (e.g., new CCF/CL tables, changed table generation behavior), you must
  preserve backward compatibility as an explicit migration contract: (1) keep stable
  customer-facing identifiers, (2) provide a compatibility access layer for both old
  and new schemas, and (3) validate the...'
repository: Azure/Azure-Sentinel
label: Migrations
language: Json
comments_count: 4
repository_stars: 6042
---

When making schema/connector changes that can affect existing customer deployments (e.g., new CCF/CL tables, changed table generation behavior), you must preserve backward compatibility as an explicit migration contract: (1) keep stable customer-facing identifiers, (2) provide a compatibility access layer for both old and new schemas, and (3) validate the migration scenario in-place.

How to apply
- Schema/table changes (CCF/CL):
  - If new table(s) are added or CL versions differ (old Azure Function creates CLV1 tables; new DCR-based/CCF deployment creates/updates as CLV2 while reusing the same name), add or update parsers so existing customer queries continue to work across both old and new table sets.
  - Follow existing connector/solution patterns for parser structure.
- In-place testing:
  - Test backward compatibility in the same workspace/subscription using the actual migration path (e.g., deploy the old connector, then deploy the CCF one into the same workspace) to confirm nothing breaks when tables with the same name behave differently.
- Migration contract/version/identifiers:
  - Do not rename stable customer-visible keys/identifiers (e.g., workbook/solution identity fields). Renaming can orphan existing deployments.
  - Use version bumps that reflect compatibility: bump minor for backward-compatible functionality; reserve major for breaking changes.

Example (parser compatibility intent)
- The goal is to ensure consumers can query one logical dataset even when underlying tables differ by CL generation.
- In practice, implement parsers (or an equivalent mapping layer) that can detect/map both the legacy and newly introduced table schemas, e.g.:

```jsonc
// Pseudocode intent: parser selects/normalizes fields from both legacy and new tables
{
  "parser": {
    "inputTables": ["LegacyTable_CL", "NewTable_CL"],
    "fieldMap": {
      "PascalCaseFieldA": "PascalCaseFieldA",
      "PascalCaseFieldB": "PascalCaseFieldB"
    },
    "normalizeTo": "LegacyCompatibleSchema"
  }
}
```

Acceptance checklist
- [ ] New/changed tables introduced by the migration are covered by parsers or equivalent compatibility mappings.
- [ ] In-place migration scenario is tested (old deployment -> CCF deployment in same workspace).
- [ ] Stable identifiers were not renamed.
- [ ] Version bump matches the backward-compatibility level.