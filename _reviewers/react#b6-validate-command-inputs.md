---
title: Validate Command Inputs
description: When security-sensitive workflow actions are triggered by user-controlled
  text (e.g., issue comment commands), don’t use broad substring checks like `contains(comment,
  '/land')`. Strictly validate/parse the command so it can’t be triggered by incidental
  matches (such as URLs containing `/land`).
repository: facebook/react#b6
label: Security
language: Yaml
comments_count: 1
repository_stars: 251888
---

When security-sensitive workflow actions are triggered by user-controlled text (e.g., issue comment commands), don’t use broad substring checks like `contains(comment, '/land')`. Strictly validate/parse the command so it can’t be triggered by incidental matches (such as URLs containing `/land`).

Apply:
- Anchor the match to the expected command form (e.g., start of comment, or a full-line command).
- Require command boundaries (e.g., `/land` as a standalone token), not arbitrary substrings.
- Treat comment body as untrusted input.

Example (GitHub Actions expression):
```yaml
# Good: match a standalone /land command at the start (or first non-whitespace token)
# (Adjust pattern to your expected format)
if: >-
  ${{
    needs.check_maintainer.outputs.is_core_team == 'true' &&
    github.event.issue.pull_request &&
    startsWith(
      github.event.comment.body && ' ' ,
      '/land'
    )
  }}
```
If you need more precision than `startsWith`, implement a stricter regex/tokenization step (e.g., via a small script) and gate the job only on an exact parsed command.