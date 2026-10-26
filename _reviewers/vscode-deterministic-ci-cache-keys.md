---
title: Deterministic CI Cache Keys
description: 'Use deterministic, content-derived cache keys and ensure every producer/consumer
  of that cache computes the key *identically*.


  Apply these rules when adding or modifying CI caching (especially GitHub Actions):'
repository: microsoft/VSCode
label: Caching
language: Yaml
comments_count: 3
repository_stars: 194303
---

Use deterministic, content-derived cache keys and ensure every producer/consumer of that cache computes the key *identically*.

Apply these rules when adding or modifying CI caching (especially GitHub Actions):
1) Key from real content inputs
- Include pinned versions and every option that changes the cache payload (e.g., Playwright version + requested browser set + OS/arch).
- Derive versions from the same lockfile used by the install.

2) Keep warm and restore in lockstep
- If a cache is “warmed” on `main`, the restore step must use the exact same key computation (including the exact strings and argument formatting) or you will get misses.
- Watch for evaluation-layer differences: GitHub expressions (`${{ }}`) are not the same as shell substitution (`$(...)`). If `key-args` is interpolated into a `run:` script, the shell will evaluate `$(...)`, so the string must match what the warming workflow uses.

3) Follow repo cache action pinning
- Reuse the same `actions/cache/restore` + `actions/cache/save` pinning pattern already used in the repo to prevent behavior drift. If you want to upgrade pins, do it as a coordinated change.

Example pattern (deterministic key + shared restore args)
```yaml
- name: Restore browsers cache
  uses: actions/cache/restore@55cc8345863c7cc4c66a329aec7e433d2d1c52a9 # v6.1.0
  with:
    path: .build/ms-playwright
    key: "playwright-v1-${{ runner.os }}-${{ runner.arch }}-${{ steps.prepare.outputs.version }}-${{ steps.prepare.outputs.browsers }}"

# Where steps.prepare computes:
# - version from the pinned lockfile
# - browsers from the install args
```

Checklist for PRs
- [ ] Does the cache key include every input that changes cached contents?
- [ ] Do warm and restore workflows compute the key the same way (including shell vs GitHub expression evaluation)?
- [ ] Are cache action versions consistent with the repo, or is this part of a coordinated pin upgrade?
