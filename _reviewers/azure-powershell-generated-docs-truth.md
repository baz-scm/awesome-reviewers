---
title: Generated docs truth
description: 'When documentation or module metadata files are produced by a generator
  (e.g., AutoRest), treat those outputs as **generated artifacts**, not as the place
  to apply fixes. Instead:'
repository: Azure/azure-powershell
label: Documentation
language: Other
comments_count: 2
repository_stars: 4762
---

When documentation or module metadata files are produced by a generator (e.g., AutoRest), treat those outputs as **generated artifacts**, not as the place to apply fixes. Instead:
1) Identify which file is generated (diffs in README scaffold/help/examples/test stubs, etc.).
2) Update the upstream generator inputs (e.g., custom folder content and the `README.md`/autorest configuration that drives generation).
3) For runtime/behavioral facts (like dependency versions), use the **authoritative** location (typically the module manifest fields such as `RequiredModules`), not incidental wording in scaffolding README.
4) Re-run the build/regeneration so outputs update consistently.

Example (PowerShell module manifest dependency truth):
```powershell
# src/SomeModule/Az.SomeModule.psd1
RequiredModules = @(
  @{ ModuleName = 'Az.Accounts'; ModuleVersion = '5.5.0' }
)
```
If you see a mismatch in a generated README scaffold line, don’t “fix the README”; fix the generator input (or the manifest field that actually drives runtime requirements) and regenerate outputs.