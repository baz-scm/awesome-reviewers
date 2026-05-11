---
title: Lockfile Change Hygiene
description: Lockfiles (e.g., pnpm-lock.yaml) are configuration artifacts and should
  only change when the dependency configuration (package.json / workspace manifests)
  changes. If there are no package.json changes, do not commit lockfile updates; treat
  any lockfile-only diffs as accidental/experimental output and revert them.
repository: tanstack/query
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 49380
---

Lockfiles (e.g., pnpm-lock.yaml) are configuration artifacts and should only change when the dependency configuration (package.json / workspace manifests) changes. If there are no package.json changes, do not commit lockfile updates; treat any lockfile-only diffs as accidental/experimental output and revert them.

How to apply:
- Before creating a PR, check what changed:
  - If only pnpm-lock.yaml changed (or shows unrelated experiment sections) and no package.json/package workspace manifests changed, revert pnpm-lock.yaml.
- If you need to test dependency resolution, do it locally and ensure the working tree doesn’t introduce lockfile-only diffs into the PR.

Example rule of thumb:
- ✅ package.json changed → lockfile may update and should be committed.
- ❌ package.json did not change → revert pnpm-lock.yaml so the PR contains only intentional configuration changes.