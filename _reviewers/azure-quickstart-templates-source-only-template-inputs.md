---
title: Source-only Template Inputs
description: Default to a single source-of-truth for infrastructure-as-code and ensure
  CI/CD owns generated deployment artifacts. This reduces drift and keeps pipeline
  behavior predictable.
repository: Azure/azure-quickstart-templates
label: CI/CD
language: Json
comments_count: 5
repository_stars: 14846
---

Default to a single source-of-truth for infrastructure-as-code and ensure CI/CD owns generated deployment artifacts. This reduces drift and keeps pipeline behavior predictable.

Apply this standard:
- If the template is authored in Bicep, commit only the `.bicep` source files; do not commit the generated `.json` deployment templates (CI should generate them).
- If a `.json` prereq/deployment file is committed but there is no corresponding Bicep source, remove any Bicep-specific generator/metadata/header that misrepresents how the file was produced.
- For deployment `validationType`/validation strategy, prefer automation; set `validationType: "Manual"` only when you can’t reliably automate due to external constraints (e.g., physical/hardware wiring) and keep the rationale explicit.

Example (Bicep-first repo pattern):
```bicep
// File: templates/deploy-devbox.bicep
// CI will generate the corresponding azuredeploy.json.
```
```json
// DO NOT commit azuredeploy.json if it is generated in CI.
// DO commit only the .bicep source plus clear metadata/justification when needed.
```

Result: PRs stay focused on intent (source), CI produces deployable artifacts (outputs), and deployment validation settings align with what the pipeline can automate.