---
title: Document Real Behavior
description: 'When updating documentation, ensure it matches actual product behavior
  and helps users predict outcomes.


  Apply this standard:

  - **No-op options/claims:** If a flag/feature “does nothing,” remove the doc entry.
  If you must keep it temporarily, label it clearly as **broken/ignored**, include
  the scope of impact, and note when/why it will change.'
repository: cline/cline#v5
label: Documentation
language: Other
comments_count: 3
repository_stars: 70864
---

When updating documentation, ensure it matches actual product behavior and helps users predict outcomes.

Apply this standard:
- **No-op options/claims:** If a flag/feature “does nothing,” remove the doc entry. If you must keep it temporarily, label it clearly as **broken/ignored**, include the scope of impact, and note when/why it will change.
- **Conditional behavior:** If behavior varies by provider/platform/config (e.g., hooks not running because the model provider performs tool handling), explain the **trigger conditions in plain language**, not just specific vendor names.
- **Call out caveats consistently:** For exceptions/limitations (timing differences, unsupported events, provider-dependent behavior), use a dedicated **“Caveats / Known limitations”** section or callout near the relevant text.
- **Keep examples consistent with `--help`/actual behavior:** Tables, option semantics, and result ordering should reflect the real command output.

Example structure for a caveat (adapt to your docs style):
```md
## Caveats
- **Provider-dependent behavior:** Some model providers may run tool handling internally, so `PreToolUse`/`PostToolUse` hooks might not execute.
- **How to tell:** Use `cline config hooks` to see which hooks the CLI detects, and verify hook execution in logs.
```

This prevents misleading documentation (“accepted but ignored”) and reduces user confusion when behavior depends on environment details.