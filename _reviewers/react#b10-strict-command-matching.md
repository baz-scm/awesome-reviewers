---
title: Strict command matching
description: When workflow logic enables privileged actions based on user-controlled
  text (e.g., issue comments), avoid broad substring checks like `contains(..., '/land')`.
  Use strict parsing that matches only the intended command (exact/anchored/regex
  with boundaries), so URLs or other text containing the substring can’t trigger the
  action.
repository: facebook/react#b10
label: Security
language: Yaml
comments_count: 1
repository_stars: 251894
---

When workflow logic enables privileged actions based on user-controlled text (e.g., issue comments), avoid broad substring checks like `contains(..., '/land')`. Use strict parsing that matches only the intended command (exact/anchored/regex with boundaries), so URLs or other text containing the substring can’t trigger the action.

Example pattern:
```yml
# Bad: could match URLs or other text containing /land
if: ${{ github.event.issue.pull_request && contains(github.event.comment.body, '/land') }}

# Better: match command only (start-of-line + exact token)
if: ${{ github.event.issue.pull_request && startsWith(github.event.comment.body, '/land') }}

# Or: match with stricter token boundaries (adjust as needed)
# if: ${{ github.event.issue.pull_request && github.event.comment.body =~ '^/land(\s|$)' }}
```
Apply this anywhere you gate sensitive operations on free-form input; combine it with existing authorization checks (e.g., member/core-team) for defense in depth.