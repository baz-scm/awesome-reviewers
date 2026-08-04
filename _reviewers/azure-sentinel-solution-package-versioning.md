---
title: Solution package versioning
description: When releasing Sentinel solutions, treat version fields (e.g., `_solutionVersion`)
  and packaging outputs as contracts with CI/CD validators and external certification/release
  systems.
repository: Azure/Azure-Sentinel
label: CI/CD
language: Json
comments_count: 4
repository_stars: 6042
---

When releasing Sentinel solutions, treat version fields (e.g., `_solutionVersion`) and packaging outputs as contracts with CI/CD validators and external certification/release systems.

**Standards**
- **Do not bump solution versions for metadata-only cert fixes.** If the change is limited to metadata (descriptions/IDs) and the external Partner Center offer is still at the old version, keep `_solutionVersion` unchanged to avoid version-mismatch failures.
- **Bump versions only for functional changes.** Use semver: metadata-only → no bump; new/extended behavior → bump (per your team’s release policy, often minor/patch depending on backward compatibility).
- **If CI fails due to generated-tool artifacts, don’t refactor the source blindly.** When an issue is known to come from the packaging tool output (e.g., unrendered `@{...}` artifacts), prefer a controlled pre-submission workaround (patch the generated `mainTemplate.json` / packaging output) rather than altering unrelated authoring files.
- **Avoid “fixing” intentional ARM escaping to satisfy superficial checks.** If the structure is known to be required for nested template evaluation and passes ARM-TTK, keep it as-is.

**Example (metadata-only fix pattern)**
```json
// Keep version locked during certification review
{
  "_solutionVersion": "3.0.0",
  "solutionId": "<metadata corrected id>"
}
// Bump _solutionVersion only when you add/alter functional content
// e.g., new analytics rule/workbook behavior after go-live
```

**Operational checklist (CI/CD)**
1. Classify the change: metadata-only vs functional.
2. Confirm external release target version (Partner Center / marketplace listing) before changing `_solutionVersion`.
3. If CI fails, identify whether it’s a packaging-generator artifact vs a real source/template authoring issue.
4. Only apply targeted workarounds to the packaging output when the root cause is tooling, not your content.