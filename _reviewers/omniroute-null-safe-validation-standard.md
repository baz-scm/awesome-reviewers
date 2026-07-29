---
title: Null-Safe Validation Standard
description: Always validate `null`/`undefined` (and malformed shapes) before dereferencing,
  filtering, or merging—treat `null` as an explicit, documented input rather than
  “missing”.
repository: diegosouzapw/OmniRoute
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 33162
---

Always validate `null`/`undefined` (and malformed shapes) before dereferencing, filtering, or merging—treat `null` as an explicit, documented input rather than “missing”.

Apply this consistently:
- **Filter/transform:** check the element exists before reading its fields; don’t rely on optional chaining alone.
- **Parse responses:** guard arrays and nested properties so malformed upstream payloads fall through to a safe result (not a throw).
- **Defaults:** handle callers passing `null` (not just omitting the argument) when reading options.
- **API semantics:** explicitly define how `null` vs `{}` vs partial objects affect state (e.g., PATCH “clear” must be explicit `null`).
- **Type narrowing:** prefer runtime guards (`typeof`, `in`, `Array.isArray`) over casts.
- **Tests:** add regression tests for `null`/empty/malformed shapes.

Example patterns:
```ts
// 1) Filtering: guard nullish elements + explicit null meaning
function filterActiveConnections<T extends { isActive?: boolean }>(connections: (T | null | undefined)[]) {
  return connections.filter((c) => !!c && c.isActive !== false);
}

// 2) Parsing: tolerate malformed upstream arrays
function extractFirstVideo(response: unknown): { base64?: string; url?: string } | null {
  if (!response || typeof response !== 'object') return null;
  const videos = (response as any).videos;
  if (!Array.isArray(videos) || videos.length === 0) return null;
  const v = videos[0] as any;
  if (typeof v?.bytesBase64Encoded === 'string') return { base64: v.bytesBase64Encoded };
  if (typeof v?.gcsUri === 'string') return { url: v.gcsUri };
  return null;
}

// 3) Options default: tolerate explicit null
export function filterToOpenAIFormat(body: unknown, opts: { preserveCacheControl?: boolean } | null = {}) {
  const preserve = opts?.preserveCacheControl === true;
  // ...
}

// 4) PATCH semantics: explicit null clears; empty object is no-op
function applyPatch(existing: any, incomingWindowThresholds: any) {
  if (incomingWindowThresholds === null) return { ...existing, quotaWindowThresholds: null };
  if (incomingWindowThresholds && typeof incomingWindowThresholds === 'object') {
    const next = { ...(existing.quotaWindowThresholds ?? {}) };
    for (const [k, v] of Object.entries(incomingWindowThresholds)) {
      next[k] = v === null ? null : v;
      if (v === null) delete next[k]; // optional: choose your clear behavior per spec
    }
    return { ...existing, quotaWindowThresholds: next };
  }
  return existing; // {} should be no-op; missing should be no-op
}
```

If a function can receive `null`/`undefined` from upstream, config, or user input, make the “what happens” path explicit and test the nullish/empty cases.