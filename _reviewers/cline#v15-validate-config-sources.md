---
title: Validate config sources
description: 'Treat configuration-related changes (schema fields, rollout/feature
  flags, packaging ignores) as *tool-derived* and *behavior-mapped* rather than ad-hoc
  edits. Always:'
repository: cline/cline#v15
label: Configurations
language: Other
comments_count: 3
repository_stars: 70877
---

Treat configuration-related changes (schema fields, rollout/feature flags, packaging ignores) as *tool-derived* and *behavior-mapped* rather than ad-hoc edits. Always:

1) Use the repository’s source of truth
- If a config schema (e.g., proto/state secrets) is generated, update the upstream definition (e.g., `state-keys.ts`) and re-run the generator—don’t manually edit generated outputs.

2) Verify with the project’s config/build checks
- After regenerating, run the repo scripts that validate consistency/types (e.g., the proto generation step and type checks).

3) Keep docs aligned with config-driven behavior
- If different builds/loaders are selected by a setting (e.g., bundle override for `next` vs `legacy`), document the exact setting key and override values, and how it affects behavior.

4) Confirm packaging assumptions against real tooling
- Don’t duplicate ignore rules “just in case.” Verify with packaging commands (e.g., `vsce ls`, packaging scripts) that redundant entries aren’t needed and that stale artifacts can’t be included.

Example (generator-first workflow for generated config/schema):
```sh
# Update the upstream source of truth (e.g., state-keys.ts)

# Regenerate derived config/schema
node scripts/generate-state-proto.mjs

# Validate
npm run protos
npm run check-types
```
This prevents config drift, incorrect secret key/index mappings, misleading rollout documentation, and packaging rules that become stale or redundant over time.