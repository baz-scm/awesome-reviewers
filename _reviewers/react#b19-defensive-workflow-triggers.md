---
title: Defensive workflow triggers
description: 'CI/CD workflow definitions must be written defensively: triggers, conditionals,
  and shell commands should fail safe and avoid unintended side effects. Specifically:'
repository: facebook/react#b19
label: CI/CD
language: Yaml
comments_count: 6
repository_stars: 251893
---

CI/CD workflow definitions must be written defensively: triggers, conditionals, and shell commands should fail safe and avoid unintended side effects. Specifically:

- Use exact or anchored matching (e.g. `startsWith`) instead of loose substring checks like `contains()` for comment/body-triggered actions, since a URL or unrelated text containing the substring could accidentally trigger a privileged action (e.g. landing a PR).
- Pick the event type that actually matches the condition you're gating on. Don't trigger on a broad event (e.g. `pull_request: opened`) and then filter by a property (e.g. a label) that is set by a separate, possibly-later workflow — this creates a race. Use the dedicated event (e.g. `labeled`) instead.
- Escape shell metacharacters (backticks, `$()`, etc.) in echoed strings used for error messages so they print literally instead of being executed by the shell.
- For `workflow_dispatch` inputs that control destructive or production-affecting behavior (e.g. an npm dist-tag), do not set a default value that could cause an accidental production action if the operator forgets to change it.
- Avoid duplicating validation that the underlying tool already performs (e.g. re-checking if a version is already published when `npm publish` already errors on that).
- When tuning caches, prefer safe degradation (e.g. dropping broad `restore-keys` fallbacks) over keeping them indefinitely, since stale or ever-growing caches can introduce subtle bugs that are worse than an occasional cache miss.

Example fix for substring matching:
```yaml
# Before: matches any comment containing "/land" anywhere, e.g. in a URL
if: contains(github.event.comment.body, '/land')

# After: only matches comments that start with the command
if: startsWith(github.event.comment.body, '/land')
```

Treat workflow YAML with the same rigor as application code — reason through race conditions, injection risks, and failure modes before merging.