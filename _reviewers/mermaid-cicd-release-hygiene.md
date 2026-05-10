---
title: CI/CD release hygiene
description: 'For any PR that affects the build/release pipeline (scripts, manifests
  like package.json, or release tooling), require:


  1) Pipeline must be green before requesting/continuing review'
repository: mermaid-js/mermaid
label: CI/CD
language: Json
comments_count: 3
repository_stars: 87952
---

For any PR that affects the build/release pipeline (scripts, manifests like package.json, or release tooling), require:

1) Pipeline must be green before requesting/continuing review
- No unexpected changes to root package manifests or release inputs unless necessary.

2) Release automation must be complete and consistent
- Include a changeset for versioned releases.
- Ensure the changeset bump type matches the intended semver outcome (don’t rely on implicit mapping).
- Include corresponding docs/changelog updates when required by the project process.

3) Local quality gates must mirror CI (or be clearly split)
- Avoid having `pnpm lint` behave differently from what CI runs.
- If you need faster local feedback, introduce explicit targets and make the default match CI.

Example script structure (align local with CI, while still allowing fast runs):
```json
{
  "scripts": {
    "lint:fast": "pnpm biome check && pnpm lint:jison",
    "lint:fast:fix": "pnpm biome check --write",
    "lint:slow": "pnpm lint:fast && cross-env NODE_OPTIONS=--max_old_space_size=16384 eslint --cache --cache-strategy content .",
    "lint": "pnpm lint:slow",
    "lint:fix": "pnpm lint:fast:fix && cross-env NODE_OPTIONS=--max_old_space_size=8192 eslint --cache --cache-strategy content --fix . && tsx scripts/fixCSpell.ts"
  }
}
```
Also update any CI workflow or automation that calls the old script names so CI and local stay in sync.

Practical checklist before merge:
- CI passes.
- package.json changes are intentional.
- changeset exists and semver intent is correct.
- required docs/changelog updates are included.
- `pnpm lint` (and other gated commands) reflect what CI enforces, or the split is explicit and workflow references are updated.