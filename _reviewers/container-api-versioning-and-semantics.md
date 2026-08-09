---
title: API Versioning And Semantics
description: 'Define and document your public API contract with two guarantees: (1)
  versioning/compatibility rules, and (2) unambiguous parameter semantics (source
  of truth and precedence). '
repository: apple/container
label: API
language: Markdown
comments_count: 2
repository_stars: 48787
---

Define and document your public API contract with two guarantees: (1) versioning/compatibility rules, and (2) unambiguous parameter semantics (source of truth and precedence). 

Apply this when publishing Swift/XPC interfaces and when documenting client-facing parameters/options (including convenience aliases).

**Versioning/compatibility**
- Follow SemVer rules for major/minor/patch releases *or* explicitly document the deviations.
- State the compatibility boundary per API surface (e.g., “XPC API compatibility is guaranteed within the same major version so older and newer clients can interoperate”).
- Define what each component of the version number means (e.g., monthly minor releases, patch releases for hotfixes).

**Parameter semantics**
- If you expose both a convenience flag and a driver/core option (e.g., `-s` and `--opt size=...`), clearly document:
  - why both exist (convenience vs underlying capability)
  - what the canonical parameter is
  - precedence when both are provided (which one “wins”).

**Example rule for precedence**
- “`-s <s>` is a convenience alias for the `size` driver option; if both `-s` and `--opt size=...` are specified, `-s` takes precedence.”

**Practical checklist**
- For each public API: publish compatibility scope per major/minor/patch.
- For each user/client input: document the source-of-truth and override/precedence behavior when duplicates are possible.