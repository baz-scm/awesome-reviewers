---
title: Package.json consistency
description: 'When editing package.json, ensure all related configuration fields stay
  in sync. Specifically: (1) Whenever a new module is added to the `exports` map,
  add a matching entry in `typesVersions` so TypeScript can resolve the types for
  that subpath, e.g. adding `"./timeout"` to `exports` requires a corresponding `"timeout":...'
repository: HONOJS/HONO
label: Configurations
language: Json
comments_count: 3
repository_stars: 32741
---

When editing package.json, ensure all related configuration fields stay in sync. Specifically: (1) Whenever a new module is added to the `exports` map, add a matching entry in `typesVersions` so TypeScript can resolve the types for that subpath, e.g. adding `"./timeout"` to `exports` requires a corresponding `"timeout": ["./dist/types/middleware/timeout/index.d.ts"]` entry in `typesVersions`. (2) If you add a temporary `overrides`/`resolutions` entry to work around an upstream dependency issue, include a comment or PR link explaining why it exists and when it can be removed, and follow up with a cleanup commit once the upstream fix is released. Treat package.json as a single source of truth where dependent fields (exports/typesVersions, dependency versions/overrides) must be reviewed together to avoid drift and leftover workarounds.</description>
</invoke>
