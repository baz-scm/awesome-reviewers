---
title: Manage Generated Configs
description: 'When working with configuration JSON files, treat them as tool- and
  schema-backed artifacts:


  - **Never manually edit auto-generated configuration/content files.** If a change
  is required, update the generator/template or revert the diff.'
repository: kamranahmedse/developer-roadmap
label: Configurations
language: Json
comments_count: 3
repository_stars: 354523
---

When working with configuration JSON files, treat them as tool- and schema-backed artifacts:

- **Never manually edit auto-generated configuration/content files.** If a change is required, update the generator/template or revert the diff.
- **Avoid direct JSON edits when the file is synchronized with an editor/tool state.** Make changes through the intended UI/tooling so the “editor state” and the “code state” remain consistent.
- **Validate config fields against the allowed schema/contract.** Ensure values use only supported options (e.g., a field whose type is restricted must not be set to an unsupported string).

Example pattern:
```json
// Bad: violates the config contract
{ "type": "DevOps Roadmap" }

// Good: use an allowed value
{ "type": "button" }
```

Process guidance:
- If a diff appears due to the tool (e.g., unexpected dimension/visual-property changes), **revert and re-apply via the supported workflow** rather than continuing manual tweaks.
- Add/enable schema validation (or a lightweight pre-commit check) so invalid configuration values fail fast before review.