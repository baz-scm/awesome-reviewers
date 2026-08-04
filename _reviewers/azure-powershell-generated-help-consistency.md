---
title: Generated Help Consistency
description: 'When changing cmdlet behavior or parameter semantics, treat help/examples
  as generated artifacts: update the source definitions/config (custom folder, README.md,
  autorest options/directives, APIspec where applicable) and then regenerate. Avoid
  hand-editing generated help/stubs, because edits will be overwritten and may desync
  parameter sets or requiredness.'
repository: Azure/azure-powershell
label: Documentation
language: Markdown
comments_count: 8
repository_stars: 4762
---

When changing cmdlet behavior or parameter semantics, treat help/examples as generated artifacts: update the source definitions/config (custom folder, README.md, autorest options/directives, APIspec where applicable) and then regenerate. Avoid hand-editing generated help/stubs, because edits will be overwritten and may desync parameter sets or requiredness.

Apply this checklist:
1) Update the correct source of truth (custom help text, autorest README/config, or APIspec/model) rather than editing generated docs directly.
2) Regenerate help/examples using the project’s generation workflow.
3) Validate generated output matches intent:
   - Parameter sets: ensure parameters only appear in the correct sets.
   - Required flags: preserve multi-block YAML patterns that intentionally vary Required per parameter-set.
   - Types/Completers: keep parameter Type and argument completers consistent with documented “Accepted values”.
   - HTTP semantics: if the API uses PUT/create-or-replace, reflect it in SYNOPSIS/DESCRIPTION (“Create or update …”).
   - Examples: pick inputs that actually demonstrate conditional/branching behavior.

Example workflow (typical):
```powershell
# 1) Edit sources (e.g., src/<service>/<client>/custom/* and the autorest README/config).
# 2) Regenerate docs
autorest & ./build-module.ps1
# 3) Verify key help semantics in generated output for the affected cmdlets.
```