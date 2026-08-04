---
title: Scoped Hash-Based Idempotency
description: When implementing idempotency or caching via markers/ledger “done” signals,
  treat cached state as valid only if (a) the key reflects the content/version being
  applied and (b) the signal is scoped to the current execution context.
repository: awslabs/aidlc-workflows
label: Caching
language: TypeScript
comments_count: 2
repository_stars: 3849
---

When implementing idempotency or caching via markers/ledger “done” signals, treat cached state as valid only if (a) the key reflects the content/version being applied and (b) the signal is scoped to the current execution context.

Apply these rules:
1) Key by content/version, not just identity.
- If you use a sentinel to decide whether a fragment/work already exists, include a content hash (or equivalent version) in the marker.
- On hash mismatch, replace/update the existing cached block instead of skipping forever.

2) Scope “done” signals to the current run window.
- If you read completion/convergence from an append-only audit/ledger, don’t treat all historical rows as applicable.
- Floor or filter the query by a stage-run boundary (e.g., the latest STAGE_STARTED timestamp/id for the current stage run) so a re-run with the same names is evaluated correctly.

3) Detect same-key conflicts and don’t fail silently.
- If two inputs produce the same cache key (e.g., same bundle+anchor+order), log a drop and fail early (or otherwise record a build error) instead of silently keeping the first.

Example (marker replacement with hash):
```ts
const markerOpen = `<!-- plugin:${bundle}:${anchor}:${order}:${hash} -->`;
const markerClose = `<!-- /plugin:${bundle}:${anchor}:${order}:${hash} -->`;

// When the marker exists with a different hash, replace the whole block.
// When the marker exists with the same hash, skip (true idempotency).
```

Example (scoping cached convergence by stage start):
```ts
// Only consider SWARM_UNIT_CONVERGED rows emitted after the current stage-run start.
const since = latestStageStartedAt;
const rows = auditRows.filter(r => r.type === 'SWARM_UNIT_CONVERGED' && r.at >= since);
const converged = new Set(rows.map(r => r.unitName));
```

Result: upgrades land correctly, re-runs don’t get incorrectly skipped, and collisions are visible—avoiding the two most common “stale cache” failure modes shown here (perma-skip on upgrade, and reuse of historical convergence across re-entry).