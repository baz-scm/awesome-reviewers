---
title: Precise command matching
description: When a workflow uses user-controlled text (e.g., issue/PR comments) to
  trigger security-sensitive actions, validate the command precisely—avoid broad substring
  checks like `contains(..., '/land')` that can be satisfied by unrelated text (such
  as a URL containing `/land`).
repository: facebook/react#b16
label: Security
language: Yaml
comments_count: 1
repository_stars: 251891
---

When a workflow uses user-controlled text (e.g., issue/PR comments) to trigger security-sensitive actions, validate the command precisely—avoid broad substring checks like `contains(..., '/land')` that can be satisfied by unrelated text (such as a URL containing `/land`).

Apply exact matching patterns (start-of-line, word boundaries, or anchored regex) so only the intended command activates the job.

Example (GitHub Actions):
```yaml
# Bad: triggers if '/land' appears anywhere (e.g., in a URL)
# if: contains(github.event.comment.body, '/land')

# Good: only triggers on an exact command token
if: startsWith(github.event.comment.body, '/land')
# or (more robust) match a command line using a regex/word-boundary approach
```