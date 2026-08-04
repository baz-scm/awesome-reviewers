---
title: Maintainable Documentation Standards
description: 'Keep template READMEs technically correct, GitHub-renderable, and maintainable.


  - Use markdown syntax that GitHub will render (avoid docs.microsoft.com-only constructs
  like `[!TIP]`; if needed, replace with standard headings/blockquote/correct GitHub-compatible
  callouts).'
repository: Azure/azure-quickstart-templates
label: Documentation
language: Markdown
comments_count: 5
repository_stars: 14846
---

Keep template READMEs technically correct, GitHub-renderable, and maintainable.

- Use markdown syntax that GitHub will render (avoid docs.microsoft.com-only constructs like `[!TIP]`; if needed, replace with standard headings/blockquote/correct GitHub-compatible callouts).
- Ensure labels/claims match the actual artifact(s) (e.g., don’t call something “ARM” if it’s explicitly “JSON”, or be precise with “ARM and bicep template”).
- Provide prerequisite commands that match likely tooling in the environment (prefer the Az module when applicable, and give concrete commands).
- Avoid large inline code in README files. Move substantial examples (YAML/scripts/manifests) into separate files under the repo and reference them.
- Avoid unnecessary template fragmentation when the workflow is inherently sequential (e.g., creating a SIM group always followed by creating SIMs—prefer a single template/flow where possible).

Example (GitHub-safe callout + externalized snippet):
```md
## Note
Azure Monitor alerts may incur charges.

See `docs/alert-sample.yml` for the sample manifest.
```
```yml
# docs/alert-sample.yml
# (sample contents here)
```

Example (tooling-appropriate prerequisites):
```powershell
# Prefer Az module cmdlets when available
Get-AzAdUser -UserPrincipalName $name
```