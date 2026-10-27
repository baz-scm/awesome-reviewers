---
title: Source metadata Null Safety
description: When creating new nodes or grouping IR by “identity” or “source” metadata,
  treat all optional location fields as nullable and never let missing (`undefined`/absent)
  values silently break invariants.
repository: facebook/react#b7
label: Null Handling
language: TypeScript
comments_count: 2
repository_stars: 251888
---

When creating new nodes or grouping IR by “identity” or “source” metadata, treat all optional location fields as nullable and never let missing (`undefined`/absent) values silently break invariants.

Apply these rules:
1) Propagate complete location offsets: If an original node has `start`/`end`, ensure node-creation helpers copy them (or explicitly set them consistently). Don’t rely on `loc` alone when downstream consumers expect offset ranges.
2) Guard nullable location fields: Before reading optional fields, check for `null/undefined`.
3) Never key maps by nullable strings: Don’t use something like `loc.identifierName` as a map key if it can be missing; missing values can collapse many distinct entries into the same bucket.
4) Use stable identifiers or typed keys: Prefer IDs (e.g., `IdentifierId`) or a key type that cannot be `undefined`. If you must account for missing data, store it in a dedicated “unknown/missing” bucket rather than conflating it with real values.

Example (avoid undefined-string map keys):
```ts
// Avoid: loc.identifierName as a key (may be undefined)
// const m = new Map<string | undefined, Place[]>();

// Prefer stable identifiers
const m = new Map<IdentifierId, Place[]>();

function addPlace(id: IdentifierId, place: Place) {
  const arr = m.get(id);
  if (arr) arr.push(place);
  else m.set(id, [place]);
}

// For missing metadata, use a separate bucket
const unknown: Place[] = [];
function addUnknown(place: Place) {
  unknown.push(place);
}
```