---
title: arm escaping and diff hygiene
description: 'When editing Azure Sentinel solution artifacts (ARM templates + nested
  CCF connector templates), treat ARM escaping and packaging output as correctness-critical
  formatting:'
repository: Azure/Azure-Sentinel
label: Code Style
language: Json
comments_count: 6
repository_stars: 6042
---

When editing Azure Sentinel solution artifacts (ARM templates + nested CCF connector templates), treat ARM escaping and packaging output as correctness-critical formatting:

- **Never “fix” double-bracket escaping.** In packaged/nested templates, keep the intentional ARM escaping pattern `[[ ... ]]`. Changing it to single-bracket `[...]` can cause expressions to evaluate at the wrong time.
  - ✅ Example (keep as-is):
    ```json
    "defaultValue": "[[newGuid()]"
    ```
  - ❌ Example (don’t change):
    ```json
    "defaultValue": "[newGuid()]" 
    ```
- **Ensure bracket symmetry/valid syntax inside ARM expressions.** Avoid partial/malformed expressions (e.g., missing closing brackets). Any edit to string fragments that contain `[`/`]` must be revalidated.
- **Preserve tool-generated boilerplate consistently.** If a parameter or template section is emitted identically by the packaging tool (e.g., `workspace-location` scaffolding), keep it byte-identical unless there’s an explicit semantic requirement to change it.
- **Minimize cosmetic diff churn in JSON.** Prefer targeted edits to the smallest semantic change (e.g., updating a single `solutionId`) instead of full rebuilds that reorder JSON keys non-deterministically.

Practical rule of thumb: if a change touches `[[`/`]` patterns or packaged ARM content, do not reformat—edit semantically, then run the repo’s validation/tests (e.g., arm-ttk/JsonFileValidation) to confirm correctness.