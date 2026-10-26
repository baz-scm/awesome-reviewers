---
title: Use correct cache scope
description: When using branch-scoped caches (e.g., for dependency caching), make
  the cache scope key match the ref GitHub uses for that event. Don’t use `github.ref_name`
  blindly—its value differs by event (and can cause cache misses). Also, for repos
  with many PRs, mitigate cache thrashing by proactively deleting branch-scoped caches
  on a faster cadence.
repository: github/docs
label: Caching
language: Markdown
comments_count: 3
repository_stars: 21111
---

When using branch-scoped caches (e.g., for dependency caching), make the cache scope key match the ref GitHub uses for that event. Don’t use `github.ref_name` blindly—its value differs by event (and can cause cache misses). Also, for repos with many PRs, mitigate cache thrashing by proactively deleting branch-scoped caches on a faster cadence.

Example (scope key derived from event):
```yaml
- name: Configure cache scope
  env:
    # For pull_request events, cache is keyed to the PR merge ref.
    # For workflow_dispatch, github.head_ref is empty, so fall back to the ref_name.
    CACHE_BRANCH: >-
      ${{ github.event_name == 'pull_request'
          && format('refs/pull/{0}/merge', github.event.pull_request.number)
          || github.ref_name }}
```

And for cache cleanup (high churn):
- Periodically delete obsolete branch-scoped caches (e.g., PR-related) more frequently than default eviction, using the `gh` CLI.