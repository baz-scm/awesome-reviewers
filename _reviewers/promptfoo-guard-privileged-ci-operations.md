---
title: Guard privileged CI operations
description: 'Workflows that hold secrets/tokens or that create, publish, or delete
  resources (registry tags, releases, packages) must never let untrusted or attacker-influenceable
  input decide when they run privileged or destructive steps. Concretely: (1) do not
  trigger token-bearing or mutating jobs on `pull_request`, since PR code/metadata
  is contributor-controlled —...'
repository: promptfoo/promptfoo
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 26565
---

Workflows that hold secrets/tokens or that create, publish, or delete resources (registry tags, releases, packages) must never let untrusted or attacker-influenceable input decide when they run privileged or destructive steps. Concretely: (1) do not trigger token-bearing or mutating jobs on `pull_request`, since PR code/metadata is contributor-controlled — restrict such jobs to `schedule`/`workflow_dispatch`/pushes on the default branch, and cover the PR-reachable logic with unit/stub tests instead; (2) never gate security- or publish-relevant conditions on user-controllable strings such as commit messages (e.g. `startsWith(github.event.head_commit.message, 'chore(main): release ')`) — any contributor can craft a matching title to bypass the check, so use a verifiable signal instead (e.g. a `release_created` output or an explicit input); (3) for destructive actions that were planned earlier (list-then-delete, build-then-publish), revalidate the target's current state immediately before acting and skip it if it has changed, because the live state can drift between planning and execution. Example of an unsafe gate to avoid:

```yaml
if: startsWith(github.event.head_commit.message, 'chore(main): release ')
```

Prefer an explicit, non-spoofable signal and keep privileged triggers off `pull_request` entirely.</description>
