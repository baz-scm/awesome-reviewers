---
title: Anchor command parsing
description: When workflow/job behavior is driven by user-controlled text (e.g., issue
  comment bodies), don’t use permissive substring checks (like `contains(body, '/land')`).
  Instead, validate that the comment contains the intended command as a standalone,
  properly positioned token (e.g., anchored at the start, or exact match), using `startsWith`
  or an anchored regex.
repository: facebook/react#b5
label: Security
language: Yaml
comments_count: 1
repository_stars: 251886
---

When workflow/job behavior is driven by user-controlled text (e.g., issue comment bodies), don’t use permissive substring checks (like `contains(body, '/land')`). Instead, validate that the comment contains the intended command as a standalone, properly positioned token (e.g., anchored at the start, or exact match), using `startsWith` or an anchored regex.

Example (GitHub Actions condition):
```yaml
# Avoid: contains(github.event.comment.body, '/land')

# Prefer exact/anchored command parsing:
if: |
  github.event.issue.pull_request &&
  (startsWith(github.event.comment.body, '/land') ||
   matches(github.event.comment.body, '^/land(\s|$)'))
```
This prevents accidental or malicious triggering when `/land` appears inside unrelated text such as URLs or longer strings.