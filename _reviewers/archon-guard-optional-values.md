---
title: Guard Optional Values
description: Treat any value that may be undefined/null (environment globals, optional
  stream handles, user config fields, optional IDs) as untrusted at the boundary.
  Use explicit checks/type guards instead of non-null assertions, and either omit
  invalid fields or return a deterministic safe failure—never let missing data crash
  module load or runtime.
repository: coleam00/Archon
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 21089
---

Treat any value that may be undefined/null (environment globals, optional stream handles, user config fields, optional IDs) as untrusted at the boundary. Use explicit checks/type guards instead of non-null assertions, and either omit invalid fields or return a deterministic safe failure—never let missing data crash module load or runtime.

Apply these patterns:
- SSR/browser globals: wrap `window`/`document` usage with `typeof ... !== 'undefined'` and avoid computing exported constants at module load.
- Streams/pipes/subprocess handles: don’t use `child.stdout!` / `child.stderr!`; guard for missing pipes and handle with a clear outcome.
- Config/input: defensively parse user config—only assign typed fields, drop unknown/invalid values, and clean arrays (trim, remove blanks, omit empty arrays). Don’t “fallback” to unrelated required identifiers.

Example (safe guards):
```ts
function getOrigin(): string {
  return typeof window !== 'undefined' ? window.location.origin : 'http://localhost:3737';
}

function safePipeToQueue(stream: NodeJS.ReadableStream | null | undefined) {
  if (!stream) {
    // deterministic safe failure path
    return { ok: false as const, reason: 'missing_stream' };
  }
  // safe to attach listeners
  return { ok: true as const };
}

function parseConfig(raw: Record<string, unknown>) {
  const out: { model?: string } = {};
  if (typeof raw.model === 'string') out.model = raw.model;
  // drop invalid/unknown fields silently
  return out;
}
```

This prevents null-reference crashes (SSR/tests), avoids fragile `!` usage, and keeps the system robust against malformed inputs.