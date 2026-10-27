---
title: Use anchored command matching
description: For security-sensitive workflow actions triggered by user-controlled
  text (e.g., issue/PR comments), validate the command precisely. Avoid broad substring
  checks like `contains(body, '/land')`, which can accidentally match URLs or unrelated
  text.
repository: facebook/react#b12
label: Security
language: Yaml
comments_count: 1
repository_stars: 251896
---

For security-sensitive workflow actions triggered by user-controlled text (e.g., issue/PR comments), validate the command precisely. Avoid broad substring checks like `contains(body, '/land')`, which can accidentally match URLs or unrelated text.

Apply this by using anchored/whole-command matching (e.g., starts-with after trimming, or a regex with boundaries) so only the intended command executes.

Example (GitHub Actions condition):
```yaml
- name: gate
  if: >-
    ${{
      github.event.issue.pull_request &&
      github.event.comment.body != '' &&
      startsWith(trim(github.event.comment.body), '/land')
    }}
```
Or with a regex-style boundary check (where supported in your expression context):
```yaml
if: ${{ github.event.issue.pull_request && match(github.event.comment.body, '^\s*/land(\b|$)') }}
```

Rule of thumb: treat comment bodies as untrusted input and require an exact/anchored command to trigger privileged actions.