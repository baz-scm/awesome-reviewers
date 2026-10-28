---
title: Guard stale async results
description: Whenever an async operation (fetch, cloud session creation, directory
  listing, branch lookup, clipboard read) can be superseded by a newer trigger or
  an invalidating event (reset, sign-out, user re-selection, `/clear`), the code must
  not let a late-arriving result overwrite fresher state. Use a generation/request
  token captured before the async call starts,...
repository: cline/cline#`sleep 4`
label: Concurrency
language: TSX
comments_count: 5
repository_stars: 70979
---

Whenever an async operation (fetch, cloud session creation, directory listing, branch lookup, clipboard read) can be superseded by a newer trigger or an invalidating event (reset, sign-out, user re-selection, `/clear`), the code must not let a late-arriving result overwrite fresher state. Use a generation/request token captured before the async call starts, bump it on any event that invalidates in-flight work, and check the token has not changed immediately before every state write that follows an `await` — not just at the end, but after each await if the function awaits more than once. Never trust a captured closure value for "the current state" across an await; read the live ref/token at the point of writing instead.

For actions that can be re-triggered concurrently by the user (double clicks, repeated key combos) and must not run twice in parallel, add a simple in-flight guard (a ref flag) that short-circuits a second call while the first is still pending, rather than trying to reconcile two overlapping results afterward.

Example pattern:
```ts
const requestId = useRef(0);

async function loadBranches(repo) {
  const id = ++requestId.current;
  const result = await fetchBranches(repo);
  if (id !== requestId.current) return; // superseded, drop it
  setBranches(result.branches);
}
```

Where derived state is cheaply recomputable from already-available data, prefer eliminating the race entirely by resolving it synchronously (e.g., derive the selected repo/branch from current props/state on every render) instead of persisting an async-computed value that could become stale. Add a regression test that starts a second operation (or triggers the invalidating event) before the first resolves, confirms the stale result is dropped, and confirms the final state reflects only the latest or invalidating action.