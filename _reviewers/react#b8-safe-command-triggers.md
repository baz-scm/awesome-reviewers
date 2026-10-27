---
title: Safe Command Triggers
description: 'When a CI/workflow uses user-controlled text (e.g., issue/PR comments)
  to authorize or trigger sensitive actions, treat that text as untrusted: (1) validate/parse
  the command strictly, and (2) safely handle/escape any special characters before
  passing into shell/script contexts.'
repository: facebook/react#b8
label: Security
language: Yaml
comments_count: 2
repository_stars: 251889
---

When a CI/workflow uses user-controlled text (e.g., issue/PR comments) to authorize or trigger sensitive actions, treat that text as untrusted: (1) validate/parse the command strictly, and (2) safely handle/escape any special characters before passing into shell/script contexts.

Apply this as a standard:
- **Strict command matching**: prefer exact/anchored command patterns over broad substring checks.
  - Avoid: `contains(comment.body, '/land')` (can match URLs or incidental text)
  - Prefer: anchored/exact matching such as `startsWith(trim(body), '/land')` or regex that only accepts `/land` as the command token.
- **Safe shell rendering**: escape characters with special shell meaning (notably backticks for command substitution) so messages/logs don’t execute unexpected commands.

Example (conceptual):
```yaml
# Don’t use broad substring match for sensitive actions
if: >-
  ${{
    needs.check_maintainer.outputs.is_core_team == 'true' &&
    github.event.issue.pull_request &&
    startsWith(trim(github.event.comment.body), '/land')
  }}
```
```sh
# Escape backticks so they are printed, not executed
echo "There was a change. Run \`yarn generate-inline-fizz-runtime\` and check in the result." 
```

This reduces the risk of accidental/unauthorized workflow execution and prevents unintended command execution due to special characters in user-controlled input.