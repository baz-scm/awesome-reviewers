---
title: Avoid manual SDK edits
description: 'When working on CI/CD pipelines, treat anything under `*Management.Sdk/Generated/*`
  (or similarly generated folders) as read-only.


  **Standard**

  - **Do not manually edit generated SDK/model files.** CI may fail and changes will
  be overwritten on the next regen.'
repository: Azure/azure-powershell
label: CI/CD
language: C#
comments_count: 3
repository_stars: 4762
---

When working on CI/CD pipelines, treat anything under `*Management.Sdk/Generated/*` (or similarly generated folders) as read-only.

**Standard**
- **Do not manually edit generated SDK/model files.** CI may fail and changes will be overwritten on the next regen.
- **If a behavior/schema needs to change, update the generation inputs** (e.g., the SDK generator configuration such as `src/<Service>.Sdk/README.md`) and then run the **full official SDK generation**.
- **Keep PRs to non-generated (PS) changes when possible**, and **rebase onto the latest official SDK regen** so generated artifacts are consistent and scenario tests pass.

**What to do instead (example pattern)**
- Bad (manual edit):
  - Edit a generated model/property directly in a `...Sdk/Generated/Models/...` file.
- Good (regenerate):
  - Update the generator inputs in the SDK README/config, then regenerate the SDK so the change is reflected consistently across all generated files.

**Impact**: prevents CI failures caused by “manual updates to generated SDK”, reduces churn, and ensures tests/playback use the same official artifacts as the build pipeline.