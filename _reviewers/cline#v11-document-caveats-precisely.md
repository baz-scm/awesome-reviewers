---
title: Document caveats precisely
description: "When documentation describes conditional/limited behavior, make the\
  \ caveat impossible to miss and avoid implying support that doesn’t exist. \n\n\
  Apply this by:"
repository: cline/cline#v11
label: Documentation
language: Other
comments_count: 2
repository_stars: 70871
---

When documentation describes conditional/limited behavior, make the caveat impossible to miss and avoid implying support that doesn’t exist. 

Apply this by:
- Use a consistent “Caveat” callout style for edge cases/limitations (e.g., providers/events where hooks won’t run, behavior that differs by platform/extension).
- In caveats, explain the *practical user impact* and the *class of cases* (not just one example). If it’s not exhaustive, say so and describe the general boundaries.
- Keep option/command reference tables strictly aligned with reality: do not label an option as “accepted but ignored.” If behavior is not supported, remove the entry or correct it to match `--help`/actual behavior.

Example (Markdown callout + precise behavior claim):

```md
::: caveat
Some model providers run tool processing internally, so the `PreToolUse`/`PostToolUse` hooks may not fire.
This applies to providers that handle tool calls themselves; other providers will trigger hooks normally.
:::
```

```md
| Option | Description |
|--------|-------------|
| --limit <count> | Maximum number of sessions to show (default: 50). `--help`/output behavior matches this. |
```

Outcome: users get clear, actionable warnings for tricky cases, and command/option docs never mislead users into expecting functionality that won’t happen.