---
title: Parse Commands Strictly
description: When using user-controlled text (e.g., issue/PR comments) to trigger
  security-sensitive actions (like deployments/land commands), don’t rely on broad
  substring checks such as `contains(...)`. Instead, validate that the input matches
  the intended command precisely (anchored/exact match), so unrelated text (e.g.,
  URLs containing `/land`) can’t accidentally...
repository: facebook/react#b11
label: Security
language: Yaml
comments_count: 1
repository_stars: 251894
---

When using user-controlled text (e.g., issue/PR comments) to trigger security-sensitive actions (like deployments/land commands), don’t rely on broad substring checks such as `contains(...)`. Instead, validate that the input matches the intended command precisely (anchored/exact match), so unrelated text (e.g., URLs containing `/land`) can’t accidentally trigger the workflow.

Example (conceptual):
```yaml
# ❌ Risky: substring matches anywhere in the comment
if: contains(github.event.comment.body, '/land')

# ✅ Safer: anchored/precise match (choose the pattern your command spec requires)
if: startsWith(github.event.comment.body, '/land')
# or use an exact/regex match per your command format
```