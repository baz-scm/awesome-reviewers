---
title: Check mode must mirror
description: When a pipeline script supports `--check`, it must validate *all* artifacts
  that the corresponding “write” path generates, using deterministic comparisons,
  and it must cover the full, intended target scope (prefer discovery over hardcoding).
repository: awslabs/aidlc-workflows
label: CI/CD
language: TypeScript
comments_count: 2
repository_stars: 3849
---

When a pipeline script supports `--check`, it must validate *all* artifacts that the corresponding “write” path generates, using deterministic comparisons, and it must cover the full, intended target scope (prefer discovery over hardcoding).

Apply this standard to any packaging/emission step that writes files under `dist/`:
1) Mirror outputs in `--check`
- Refactor the generation into a pure/deterministic builder (e.g., `buildPluginProjection()`), then:
  - `emit*()` writes to the real output directory.
  - `check*()` writes the same results to a temp directory and byte-compares against the committed `dist/...` tree.
- Ensure missing/different/orphaned files are reported (not just a “happy-path” diff).

2) Derive emission targets from manifests
- Don’t hardcode partial sets of harness/plugin targets when harnesses are discovered elsewhere.
- Prefer deriving targets from the same discovery step (e.g., harness manifests) so adding a new harness automatically gets the correct projections.
- Add/maintain CI assertions that verify the expected complete output set.

Example pattern (deterministic temp-dir + byte-compare):
```ts
function buildPluginProjection(/* inputs */) {
  // return a deterministic in-memory representation or write to a given dir
}

function emitPlugins(targets: string[]) {
  // write to dist/plugins/... (real output)
}

function checkPlugins(targets: string[]) {
  const tmp = /* create temp dir */;
  // write projections to tmp
  // byte-compare tmp vs dist/plugins/
  // report MISSING / DIFFERS / ORPHAN
}

if (argv[0] === '--check') checkPlugins(targets);
else emitPlugins(targets);
```

This prevents CI from passing when committed artifacts (like plugin projections) are stale, tampered, missing, or incomplete.