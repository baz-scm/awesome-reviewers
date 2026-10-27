---
title: Precision In Workflow Triggers
description: 'When workflow behavior depends on event text (issue comments, bodies,
  etc.) or embeds user-influenced strings into shell commands/logs, treat that text
  as untrusted and handle it with *precision*:'
repository: facebook/react#b9
label: Security
language: Yaml
comments_count: 2
repository_stars: 251891
---

When workflow behavior depends on event text (issue comments, bodies, etc.) or embeds user-influenced strings into shell commands/logs, treat that text as untrusted and handle it with *precision*:

- **Use strict matching for trigger phrases**: avoid broad substring checks like `contains(..., '/land')` when incidental substrings (e.g., URLs containing `/land`) could accidentally satisfy the condition. Prefer anchored checks (e.g., start-of-comment, exact command match, or regex with word/line boundaries).
- **Escape shell-special characters in CI scripts**: if you intend to display a command in an error message (using backticks for formatting), escape backticks so they aren’t interpreted as command substitution.

Example patterns:

```yaml
# Prefer anchored/exact match over substring
if: >-
  ${{
    needs.check_maintainer.outputs.is_core_team == 'true' &&
    github.event.issue.pull_request &&
    startsWith(github.event.comment.body, '/land')
  }}
```

```bash
# Escape backticks so they are printed, not executed
git diff --exit-code || (
  echo "There was a change to the Fizz runtime. Run \`yarn generate-inline-fizz-runtime\` and check in the result." && false
)
```

Apply this standard anywhere event-derived text influences control flow, gating, or shell evaluation to reduce the risk of unintended execution or mis-triggering.