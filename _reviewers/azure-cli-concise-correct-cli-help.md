---
title: Concise, Correct CLI Help
description: 'CLI help (per-flag short summaries, long summaries, and examples) must
  be readable, consistent, and executable.


  Apply these rules:

  - **Keep per-flag short text short:** Use a single, accurate sentence (with the
  default when appropriate). Do not exceed the short-help “lane” (avoid overflow).'
repository: Azure/azure-cli
label: Documentation
language: Python
comments_count: 8
repository_stars: 4592
---

CLI help (per-flag short summaries, long summaries, and examples) must be readable, consistent, and executable.

Apply these rules:
- **Keep per-flag short text short:** Use a single, accurate sentence (with the default when appropriate). Do not exceed the short-help “lane” (avoid overflow).
- **Keep related flags consistent:** If one flag introduces a new/recommended configuration path, the other related flags should point users to it (briefly), and the detailed migration guidance should live in **long help or examples**, not in each flag’s one-liner.
- **Move complexity out of `help=` strings:** Prefer `_help.py` long-summary and/or examples for detailed behavior, migration notes, and edge cases.
- **Validate help examples:** Every example in `_help.py` must be a real command with real arguments (no imaginary/renamed flags). Keep quoting shell-safe where needed.
- **Avoid problematic formatting:** Don’t use Markdown emphasis/blocks in in-tool help; prefer plain text and inline code formatting only.
- **Edit the right help source:** Place changes in the correct module (`_params.py` vs `_help.py`) so the rendered help matches the intended text.
- **Shell quoting notes:** When a note differs by PowerShell quoting (e.g., `""` vs `''`), use the correct form and consider centralizing recurring guidance instead of repeating it in every flag.

Example (pattern):
- Short per-flag help: 
  - `short-summary: Choose the maintenance schedule type. Default: Weekly."
- Migration/detail moved to examples/long summary:
  - Provide a single canonical example using `--schedule-type Weekly` with the newer maintenanceWindow flags, rather than adding long guidance to `--weekday`/`--start-hour` one-liners.