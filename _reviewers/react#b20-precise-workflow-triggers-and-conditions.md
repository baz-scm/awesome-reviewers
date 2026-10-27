---
title: Precise workflow triggers and conditions
description: 'Workflow conditions, event triggers, and inline shell commands must
  be precise to avoid unintended execution or race conditions. Specifically:


  - Avoid loose substring matching (e.g. `contains()`) for command-like triggers (e.g.
  `/land` in a comment), since unrelated text (like a URL containing that substring)
  could falsely trigger sensitive actions. Prefer...'
repository: facebook/react#b20
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 251895
---

Workflow conditions, event triggers, and inline shell commands must be precise to avoid unintended execution or race conditions. Specifically:

- Avoid loose substring matching (e.g. `contains()`) for command-like triggers (e.g. `/land` in a comment), since unrelated text (like a URL containing that substring) could falsely trigger sensitive actions. Prefer exact or anchored matching such as `startsWith()` or an exact equality check.
- Choose the correct GitHub event for the condition being checked. For example, don't key off `pull_request: opened` plus a label condition to detect "PR was labeled X" — this races against the separate event that actually applies the label. Use the dedicated event (e.g. `pull_request: labeled`) that matches the semantics you intend, even if it triggers more often.
- When embedding shell commands inside echo/error messages (e.g. backticked commands like `` `yarn generate-inline-fizz-runtime` ``), escape special characters so the shell prints them literally instead of executing them as a command substitution.

Example fix for substring matching:
```yaml
# Bad: matches any comment containing "/land" anywhere, e.g. a URL
if: contains(github.event.comment.body, '/land')

# Good: only matches when the comment body is exactly the command
if: github.event.comment.body == '/land'
```

Example fix for shell escaping:
```bash
# Bad: backticks get executed by the shell
echo "Run `yarn generate-inline-fizz-runtime` and check in the result."

# Good: backticks are escaped and printed literally
echo "Run \`yarn generate-inline-fizz-runtime\` and check in the result."
```

Always reason through how a condition or trigger could be satisfied unintentionally (malicious input, timing/race with another event, shell interpretation) before merging workflow changes.</description>
</invoke>
