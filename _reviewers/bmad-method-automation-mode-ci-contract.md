---
title: Automation Mode CI Contract
description: 'When authoring/editing CI-driven “step” scripts for automation, treat
  `{auto_mode}` as a strict, schema-driven contract:


  - **No interactive dead-ends:** In `{auto_mode}`, avoid halting/asking. If the invocation
  (e.g., spec file or staged changes context) lets you infer intent, select the correct
  option automatically; only prompt if inference truly fails.'
repository: bmad-code-org/bmad-method
label: CI/CD
language: Markdown
comments_count: 3
repository_stars: 51859
---

When authoring/editing CI-driven “step” scripts for automation, treat `{auto_mode}` as a strict, schema-driven contract:

- **No interactive dead-ends:** In `{auto_mode}`, avoid halting/asking. If the invocation (e.g., spec file or staged changes context) lets you infer intent, select the correct option automatically; only prompt if inference truly fails.
- **Non-interactive control flow:** Follow the automation rules exactly (e.g., apply patches without presenting menus; ensure required sections are skipped when specified).
- **Write required CI artifacts/results:** After the automated run, emit the expected result JSON (using the schema) and end the turn deterministically.
- **Match the machine-readable schema precisely:** If the CI gate reads from YAML frontmatter, instructions must reference the **frontmatter fields** (e.g., `status:`) rather than human markdown headings.
- **Avoid ambiguous rule references:** When citing automation rules, reference them unambiguously (e.g., with explicit relative paths) so validators/linters don’t misinterpret prose.

Example (schema-correct automation status instruction):
```md
# Wrong (human-only wording):
# Update the "Status section" to done/in-progress

# Correct (schema-driven wording):
Update the spec's YAML frontmatter `status:` field to `done`/`in-progress`.
```

Example (intent inference to avoid blocking):
```text
If invocation indicates “code-review staged changes”
→ auto-select the corresponding review option and proceed
instead of asking “What do you want to review?”
```