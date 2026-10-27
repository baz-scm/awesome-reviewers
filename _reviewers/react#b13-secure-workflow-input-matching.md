---
title: Secure Workflow Input Matching
description: Treat workflow triggers and CI script strings (e.g., GitHub comment bodies,
  event payloads) as untrusted input. Use precise, unambiguous matching for authorization
  gates, and safely quote/escape any dynamic text used in shell commands to prevent
  unintended triggering or execution.
repository: facebook/react#b13
label: Security
language: Yaml
comments_count: 2
repository_stars: 251894
---

Treat workflow triggers and CI script strings (e.g., GitHub comment bodies, event payloads) as untrusted input. Use precise, unambiguous matching for authorization gates, and safely quote/escape any dynamic text used in shell commands to prevent unintended triggering or execution.

Apply:
- Prefer exact/anchored checks over broad substring checks for user-controlled commands.
- When embedding literal text into shell commands, escape characters (like backticks) and use quoting so the shell prints text rather than interpreting it.

Example (workflow gate):
```yaml
# Instead of: contains(github.event.comment.body, '/land')
# Use anchored matching so URLs/embedded text don't trigger.
if: ${{
  needs.check_maintainer.outputs.is_core_team == 'true' &&
  github.event.issue.pull_request &&
  startsWith(trim(github.event.comment.body), '/land')
}}
```

Example (shell-safe message text):
```bash
git diff --exit-code || (
  echo "There was a change. Run \`yarn generate-inline-fizz-runtime\` and check in the result." && false
)
```