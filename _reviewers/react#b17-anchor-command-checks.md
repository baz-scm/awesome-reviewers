---
title: Anchor command checks
description: When triggering security- or authorization-sensitive automation from
  user-controlled text (e.g., issue/pull request comments), do not use permissive
  substring matching. Treat the comment body as untrusted input and only match the
  intended command format (e.g., exact token, anchored prefix, or a strict regex).
  Keep authorization/role checks as a separate...
repository: facebook/react#b17
label: Security
language: Yaml
comments_count: 1
repository_stars: 251891
---

When triggering security- or authorization-sensitive automation from user-controlled text (e.g., issue/pull request comments), do not use permissive substring matching. Treat the comment body as untrusted input and only match the intended command format (e.g., exact token, anchored prefix, or a strict regex). Keep authorization/role checks as a separate gate.

Example (replace permissive `contains`):
```yaml
# Prefer anchored matching of the actual command
if: >-
  ${{
    needs.check_maintainer.outputs.is_core_team == 'true' &&
    github.event.issue.pull_request &&
    startsWith(github.event.comment.body, '/land')
  }}
```
If commands may include whitespace or arguments, use a strict pattern instead of substring checks, e.g., match `^/land(\s|$)`.

This prevents accidental (or malicious) triggering from unrelated text such as URLs containing `/land`.