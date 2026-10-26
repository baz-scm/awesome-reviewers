---
title: Truthful CLI Documentation
description: 'Ensure documentation precisely matches runtime behavior and is written
  for the reader’s next action.


  Apply this by:

  - **Remove or fix no-ops:** If a documented flag/setting has no effect, don’t label
  it as “accepted but ignored” in user-facing docs. Either remove the doc entry or
  fix the product so the option works.'
repository: cline/cline#v7
label: Documentation
language: Other
comments_count: 4
repository_stars: 70865
---

Ensure documentation precisely matches runtime behavior and is written for the reader’s next action.

Apply this by:
- **Remove or fix no-ops:** If a documented flag/setting has no effect, don’t label it as “accepted but ignored” in user-facing docs. Either remove the doc entry or fix the product so the option works.
- **Validate CLI examples against parsing:** Examples must reflect how the CLI actually routes arguments (e.g., where channel vs options appear) and must match what `--help` and behavior imply.
- **Document structured output for consumers:** For formats like `--json`, document the actual object shape and clearly state what types/fields scripts should use, and what they can safely skip.

Example pattern (avoid misleading options; align examples):
```mdx
<!-- Bad: implies the option works when it doesn't -->
| `SOME_FLAG` | Additional hooks directory |

<!-- Good: remove or only keep if behavior is implemented -->
<!-- If not implemented, delete the row or fix the CLI first -->
```

```bash
# Good: option placement matches actual argument routing
cline connect telegram --restart -k <BOT-TOKEN>
```