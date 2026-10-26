---
title: Strict Command Matching
description: When using user-controlled text (e.g., issue/PR comments) to authorize
  or trigger security-sensitive workflow actions, do **not** rely on broad substring
  checks like `contains()`.
repository: facebook/react#b2
label: Security
language: Yaml
comments_count: 1
repository_stars: 251882
---

When using user-controlled text (e.g., issue/PR comments) to authorize or trigger security-sensitive workflow actions, do **not** rely on broad substring checks like `contains()`.

Instead, validate the command with a strict match that reflects the intended syntax (e.g., require the command at the start of the comment, whole token match, or an exact command line). This prevents accidental or malicious triggers when the keyword appears inside URLs or other unrelated text.

Example pattern:
```yaml
# Avoid:
# if: ${{ ... && contains(github.event.comment.body, '/land') }}

# Prefer: command must be at the start (or otherwise strictly formatted)
if: ${{ needs.check_maintainer.outputs.is_core_team == 'true' && github.event.issue.pull_request && startsWith(github.event.comment.body, '/land') }}
```
If you need more precision, use regex/whole-token matching (implemented via the workflow expression language or a small script) so only the exact intended command activates the job.