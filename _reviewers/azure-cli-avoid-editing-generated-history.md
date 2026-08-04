---
title: Avoid editing generated history
description: If a file is explicitly documented (or implied by the repo’s process)
  as auto-generated—such as changelog/history files—do not manually edit it in code
  changes. Instead, revert those edits and update the upstream inputs that drive generation
  (e.g., PR release-note metadata, templates, or generator configuration), then confirm
  the regenerated output contains...
repository: Azure/azure-cli
label: Documentation
language: Other
comments_count: 2
repository_stars: 4592
---

If a file is explicitly documented (or implied by the repo’s process) as auto-generated—such as changelog/history files—do not manually edit it in code changes. Instead, revert those edits and update the upstream inputs that drive generation (e.g., PR release-note metadata, templates, or generator configuration), then confirm the regenerated output contains the desired entry.

Example (what to do in PRs):
- Revert direct edits to `src/azure-cli/HISTORY.rst`.
- Add the intended item through the project’s release-note mechanism so the next automated generation produces the entry.
- Re-run/verify the generation step (or wait for CI) rather than hand-crafting the final HISTORY text.