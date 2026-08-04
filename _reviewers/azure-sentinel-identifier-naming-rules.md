---
title: Identifier Naming Rules
description: 'Use a single, deterministic naming scheme for every content identifier,
  and follow the validator’s allowed formats.


  Apply these rules:

  1) Follow exact format/allowed-value rules for metadata/ids'
repository: Azure/Azure-Sentinel
label: Naming Conventions
language: Json
comments_count: 11
repository_stars: 6042
---

Use a single, deterministic naming scheme for every content identifier, and follow the validator’s allowed formats.

Apply these rules:
1) Follow exact format/allowed-value rules for metadata/ids
- publisherId/offerId: use documented lowercase pattern like `^[a-z][a-z0-9]{0,49}$`.
- offerId: don’t include duplicated publisher prefixes; ensure the resolved full id matches the expected `publisherId.offerId`.
- Entity types/enums: use only allowed values (e.g., DNS as `dnsresolution`).
- Connector definition `id`: use the agreed pattern (e.g., `ProviderNameApplianceName`).

2) Enforce casing conventions for content fields
- Tables: use PascalCase (avoid mixing underscore-separated tokens with PascalCase styles). Prefer consistent variants (e.g., `QualysHostDetectionV2_CL`).
- Columns: use PascalCase and include a `description` for each column.

3) Treat stable customer keys as immutable
- Do not rename stable keys used for upgrade/deployment continuity (e.g., workbookKey, solutionId-like keys). You may rebrand display strings, but keep the stable identifiers unchanged.

4) Handle reserved words and mapping consistency
- If a field name is reserved (e.g., `title`), escape/quote consistently in the schema and keep the KQL transform aligned.

Example patterns
- Metadata ids:
  - Good: `"publisherId": "securityscorecard", "offerId": "securityscorecard"` (lowercase, regex-safe)
- Entity types:
  - Good: `"entities": ["dnsresolution", "IP", "URL"]`
- Table/column:
  - Good: `"name": "QualysHostDetectionV2_CL"` and column `"name": "TimeGenerated"` (PascalCase) with `description`.
- Reserved word escaping:
  - DCR column: `{ "name": "['title']", "type": "string" }`
  - Transform/KQL: map the escaped field to the desired output column consistently (including `TimeGenerated` when required).

5) Don’t “simplify” deterministic packaging outputs
- If naming expressions are generated to ensure idempotent upgrades (often version-suffixed), keep them as produced; changes can break upgrade behavior.
