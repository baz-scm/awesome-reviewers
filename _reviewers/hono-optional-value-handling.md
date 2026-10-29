---
title: Optional value handling
description: 'When a value can legitimately be `undefined`/`null` at runtime, make
  sure both the type signature and the code reflect that, and access it safely:


  - Type values correctly: if a function/property can return `undefined` (e.g. a missing
  route match, a header lookup, a route param), its type must include `| undefined`
  (or `| null`) rather than being asserted...'
repository: honojs/hono
label: Null Handling
language: TypeScript
comments_count: 13
repository_stars: 32741
---

When a value can legitimately be `undefined`/`null` at runtime, make sure both the type signature and the code reflect that, and access it safely:

- Type values correctly: if a function/property can return `undefined` (e.g. a missing route match, a header lookup, a route param), its type must include `| undefined` (or `| null`) rather than being asserted as non-nullable. Fix the types instead of hiding the gap with a non-null assertion (`!`).
- Prefer optional chaining and nullish coalescing (`?.`, `??`) over non-null assertions or `||` when a value may legitimately be an empty string, `0`, or `false` (which `||` would incorrectly treat as missing).
- Don't rely on a single default object to cover partial options; destructuring an options object with one overall default breaks down once only some fields are supplied. Give each optional field its own fallback instead:
  ```ts
  // Avoid:
  const options: Options = { all: false, dot: false }
  const parseBody = (opts: Options = options) => { ... }

  // Prefer:
  const parseBody = (opts?: Options) => {
    const all = opts?.all ?? false
    const dot = opts?.dot ?? false
  }
  ```
- When narrowing a union of shapes with differing optional fields (e.g. two event formats), use discriminating checks like `'prop' in event` rather than chaining `?.` across incompatible shapes, since optional chaining can silently resolve to `undefined` even when the correct sibling property exists under a different key.
- Guard against falsy/absent optional fields before operating on them (e.g. check `event.queryStringParameters` before calling `Object.entries` on it, or check `event.headers` before iterating), instead of assuming they are always present.
- Remove redundant null checks when a value has already been verified not to be null/undefined earlier in the same code path.
- Never use `undefined` as a sentinel/cache value when `undefined` is also a valid resolved value (e.g. caching a promise result); use a distinct marker so legitimate `undefined` results aren't mistaken for "not yet set".

Applying these practices keeps types trustworthy, avoids runtime crashes from unchecked optional access, and prevents subtle bugs caused by treating falsy-but-valid values (empty string, `false`) as missing.