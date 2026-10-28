---
title: Validate generated and scoped config
description: Configuration artifacts often have a canonical source of truth or are
  governed by external tooling defaults, and many settings are build- or environment-scoped.
  Don't hand-edit or assume behavior — verify.
repository: cline/cline#;sleep 4;
label: Configurations
language: Other
comments_count: 3
repository_stars: 70976
---

Configuration artifacts often have a canonical source of truth or are governed by external tooling defaults, and many settings are build- or environment-scoped. Don't hand-edit or assume behavior — verify.

- For generated config/proto files (e.g. `state.proto` derived from `state-keys.ts`), never hand-edit the output. Re-run the generator (e.g. `node scripts/generate-state-proto.mjs`, then `npm run protos && npm run check-types`) and confirm it produces no unexpected diff before merging.
- Before adding or removing entries in packaging/ignore config (e.g. `.vscodeignore`), check whether the underlying tool already enforces the same rule (e.g. vsce's built-in `**/*.vsix` exclusion). Verify empirically (e.g. `vsce ls`) rather than assuming redundancy or necessity.
- For feature flags or settings that vary by build/environment (e.g. `cline.rollout.bundleOverride` vs `cline-nightly.rollout.bundleOverride`), ensure keys are explicitly namespaced per variant and that documentation/code covers every variant — a key name derived from one environment's identity can silently fail or misbehave in another (e.g. Nightly vs stable).

Applying this prevents stale or redundant config, silent misconfiguration across environments, and manual edits that drift from the generated source of truth.