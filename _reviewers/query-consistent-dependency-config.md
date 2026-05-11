---
title: Consistent dependency config
description: Maintain configuration consistency and compatibility by using a single,
  intentional strategy for dependency declarations, peer ranges, and script runtimes.
repository: tanstack/query
label: Configurations
language: Json
comments_count: 12
repository_stars: 49380
---

Maintain configuration consistency and compatibility by using a single, intentional strategy for dependency declarations, peer ranges, and script runtimes.

Apply these rules:
1) Pick a monorepo pattern per package type
- Internal packages: use `workspace:*` (so pnpm rewrites correctly) when the package is meant to work inside the workspace.
- Public/example packages: keep existing semver patterns; don’t introduce `workspace:*` in examples if the repo’s established convention is semver.

2) Prefer package-local dependency ownership
- If a package imports something at runtime, declare it in that package’s `dependencies`/`peerDependencies` (avoid relying on root `devDependencies`).

3) Use `peerDependencies` when you don’t bundle
- If your package primarily exposes types or relies on a host app to provide the dependency, declare it as a `peerDependency` (and match the repo’s compatibility range).

4) Make peer semver ranges explicit and future-proof
- Avoid awkward ranges that exclude supported majors.
- For platform integrations (e.g., Next), prefer “fail fast” ranges that reflect supported versions.

5) Don’t duplicate tooling already provided by shared configs
- If a shared config already supplies lint/typescript-eslint, avoid adding redundant devDependencies in each package.

6) Use the correct TS/script runner for the declared Node environment
- If Node doesn’t support TS natively, run TS scripts via `tsx`.

Example (peer range + script runner):
```json
{
  "peerDependencies": {
    "next": "^13 || ^14",
    "typescript": "^5.0.0"
  },
  "scripts": {
    "verify-links": "pnpm tsx scripts/verify-links.ts"
  }
}
```
Example (workspace dep):
```json
{
  "dependencies": {
    "@tanstack/query-core": "workspace:*"
  }
}
```