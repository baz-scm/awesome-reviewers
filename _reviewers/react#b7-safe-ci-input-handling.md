---
title: Safe CI Input Handling
description: 'When CI/workflow behavior depends on user-provided text (e.g., issue
  comments), treat it as untrusted input: use precise matching for control-flow and
  escape shell metacharacters when composing commands/messages.'
repository: facebook/react#b7
label: Security
language: Yaml
comments_count: 2
repository_stars: 251888
---

When CI/workflow behavior depends on user-provided text (e.g., issue comments), treat it as untrusted input: use precise matching for control-flow and escape shell metacharacters when composing commands/messages.

Apply two rules:
1) Use strict/anchored command matching for workflow triggers
- Avoid broad substring checks like `contains(comment, "/land")` when the same string could appear inside URLs or unrelated text.
- Prefer an anchored pattern such as starting-with, line-bounded matching, or a regex that only accepts the intended command.

Example:
```yaml
# Instead of: contains(github.event.comment.body, '/land')
# Prefer anchored matching (example using a regex)
if: ${{ needs.check_maintainer.outputs.is_core_team == 'true' &&
        github.event.issue.pull_request &&
        matches(github.event.comment.body, '^\\s*/land(\\s|$)') }}
```

2) Escape shell metacharacters in CI scripts
- If you echo or embed instructions that include backticks (or other shell operators), escape them so they are treated as literal text and cannot be evaluated by the shell.

Example:
```sh
echo "There was a change. Run \`yarn generate-inline-fizz-runtime\` and check in the result." 
```

These practices prevent unintended job execution and accidental command evaluation—common security pitfalls in automation pipelines.