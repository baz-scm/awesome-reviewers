---
title: Document Behavioral Accuracy
description: 'All documentation should reflect the product’s real, current behavior
  and tell consumers what they can safely rely on.


  Apply these rules:

  - **No-op features/flags:** If a documented setting has “no effect,” either **remove
  it from the docs** or **fix the product**. If fixing is non-trivial, document an
  explicit caveat (what’s broken and the expected...'
repository: cline/cline#v14
label: Documentation
language: Other
comments_count: 3
repository_stars: 70876
---

All documentation should reflect the product’s real, current behavior and tell consumers what they can safely rely on.

Apply these rules:
- **No-op features/flags:** If a documented setting has “no effect,” either **remove it from the docs** or **fix the product**. If fixing is non-trivial, document an explicit caveat (what’s broken and the expected direction/timeline).
- **Keep examples executable:** CLI examples must follow the actual argument/flag parsing rules. If an option doesn’t reach the intended subcommand when placed after a channel/positional arg, the docs must show the correct ordering and (if helpful) explain why.
- **Machine-readable formats:** For extensible outputs (e.g., JSON lines), document the **contract** (what fields mean, where timestamps come from, what `type` values exist) and instruct consumers how to handle **unknown/unused types** (e.g., “skip types you don’t use”), rather than claiming exhaustive coverage.

Example (extensible JSON lines guidance):
```md
With `--json`, the CLI prints one JSON object per line.
Each line includes `type`. Scripts should **only parse the types they use** and ignore other types.
Common `type` values include: `agent_event`, `hook_event`, `team_event`, `run_result`.
```

These checks reduce “silly” dead documentation, prevent incorrect usage copy/pastes, and make docs reliable for both humans and automation.