---
title: Guard stale async results
description: Async operations (fetches, refreshes, directory/file reads, clipboard
  reads, repository/branch lookups) can resolve after a newer operation has started
  or after the user has already moved on (cleared state, signed out, switched selection).
  Writing a stale result on top of fresher state causes bugs like reattaching to an
  old session, reapplying a signed-out...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Concurrency
language: TSX
comments_count: 8
repository_stars: 70973
---

Async operations (fetches, refreshes, directory/file reads, clipboard reads, repository/branch lookups) can resolve after a newer operation has started or after the user has already moved on (cleared state, signed out, switched selection). Writing a stale result on top of fresher state causes bugs like reattaching to an old session, reapplying a signed-out user's data, or losing a newer file listing.

Protect every async write with one of these patterns, matching the shape already used across the codebase:

1. **Generation/version counters** – before starting an async call, capture (or increment) a counter tied to the resource being fetched. After the await resolves, compare the captured value to the current counter; only apply the result if they still match. Bump the counter whenever the underlying context changes (sign-out, reset, new selection, cache invalidation).

```ts
const generationRef = useRef(0);

async function refresh() {
  const generation = ++generationRef.current;
  const result = await fetchData();
  if (generation !== generationRef.current) return; // superseded, drop it
  applyResult(result);
}

function reset() {
  generationRef.current++; // invalidate any in-flight work
}
```

2. **In-flight dedup guards** – when an async action (e.g. a clipboard read, a pending create) must not run twice concurrently, store a ref/flag or the in-flight promise itself, short-circuit new calls while it's pending, and release the guard once settled so legitimate follow-up calls can proceed. Where multiple call sites can trigger the same async start (e.g. two rapid submits), funnel them through a single shared promise so only one underlying operation is created and subsequent callers await the same result.

3. **Prefer eliminating the race entirely** when possible: keep a single source of truth owned by one side (e.g. resolve derived state from authoritative data on every update instead of computing and persisting it from multiple async paths), so there's no window for a stale write to reassert itself.

When reviewing or writing code with concurrent async flows, ask: "can an older response land after a newer one, or after the user has changed context?" If yes, add a generation check, an in-flight guard, or restructure to avoid the race, and add a test that resolves the stale call last to prove it has no effect.