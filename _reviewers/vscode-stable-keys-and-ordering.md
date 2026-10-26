---
title: Stable Keys and Ordering
description: When code derives behavior (actions, dedupes, counts, ordering) from
  collections, make the algorithm deterministic by using stable identifiers and centralized
  predicate/key logic—never by relying on mutable positional indexes or ad-hoc normalization
  scattered across call sites.
repository: microsoft/VSCode
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 194303
---

When code derives behavior (actions, dedupes, counts, ordering) from collections, make the algorithm deterministic by using stable identifiers and centralized predicate/key logic—never by relying on mutable positional indexes or ad-hoc normalization scattered across call sites.

Apply these rules:
- Resolve user actions via stable IDs: if a UI “result” or summary triggers “View Changes”, include the relevant activity/item IDs in the summary state and resolve by ID at click time (or disable/clear the action when the underlying items change).
- Use a single canonical key function for identity/dedupe: define `getXKey(...)` (or equivalent) and reuse it everywhere that compares, dedupes, or builds identity-based sets/maps. Put all normalization rules (case, trailing slashes, query normalization, commit-hash handling, etc.) in that one place, with tests for “should be different” and “should be same”.
- Keep derived metrics consistent: if you show “pending vs complete” text and counts, derive both from the same predicate (or explicitly treat skipped separately).
- Centralize ordering: use explicit order arrays/constants and filter based on defined availability/policy rules, rather than sorting ad-hoc in multiple places.

Example patterns:
- Stable ID in summary state:
```ts
// summary state produced by migration engine
type Result = { migratedCount: number; activityIds: readonly string[] };

// later: resolve only the IDs captured at creation time
function openViewChanges(result: Result, activitiesById: Map<string, Activity>) {
  const activities = result.activityIds.map(id => activitiesById.get(id)).filter(Boolean);
  // open UI with `activities` (not activities[0])
}
```
- Canonical dedupe key:
```ts
function getSessionArtifactKey(artifact: ISessionArtifact): string {
  // All normalization rules live here (files/URIs vs GitHub links vs commit hashes)
  // so every dedupe/match uses the same identity.
  return /* ... */;
}

const seen = new Set<string>();
for (const a of artifacts) {
  const key = getSessionArtifactKey(a);
  if (seen.has(key)) continue;
  seen.add(key);
}
```
- Centralized ordering with explicit constants:
```ts
const ORDER = [Level.Default, Level.Assisted, Level.AutoApprove, Level.Autopilot];
const offered = ORDER.filter(l => available.includes(l) || unavailable.some(u => u.level === l));
```