---
title: Document caveats accurately
description: 'When documenting behavior, never leave exception cases implicit.


  **Standard**

  1. **Use a dedicated “Caveats” (callout) section/table** for any rule that has exceptions,
  ignored inputs, timeouts, or different behavior by environment (CLI vs extension
  vs provider, OS, etc.).'
repository: cline/CLINE
label: Documentation
language: Other
comments_count: 2
repository_stars: 70839
---

When documenting behavior, never leave exception cases implicit.

**Standard**
1. **Use a dedicated “Caveats” (callout) section/table** for any rule that has exceptions, ignored inputs, timeouts, or different behavior by environment (CLI vs extension vs provider, OS, etc.).
2. **Explain the “why,” not just the symptom**: describe the *class of conditions* that causes the exception (e.g., provider/tooling that runs parts internally), not only a potentially non-exhaustive list.
3. **Match the real contract**: options and fields must reflect actual behavior. If something is misleading (e.g., “accepted but ignored”), remove the row or explicitly omit it rather than encouraging incorrect usage.
4. **Keep tables/examples consistent** with `--help`/actual semantics (e.g., ordering, defaults, return formats).

**Example (docs pattern)**
```md
## Caveats
- **Hooks won’t run** when the model-provider executes tool processing internally.
- Only events `PreToolUse` / `PostToolUse` accept replies in the CLI+Desktop; other events start asynchronously and their replies are ignored.
```

**Example (option table correction)**
- If `--limit` semantics differ (e.g., newest-first), update the table text rather than leaving it ambiguous.
- If an option is “accepted but ignored,” remove or revise the documentation entry to prevent users from relying on it.