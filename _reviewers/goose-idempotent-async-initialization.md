---
title: Idempotent Async Initialization
description: When async flows drive UI state (events, config reads, resume/load),
  never assume timing/order will be favorable. Make initialization idempotent and
  conditionally applied so missed/early events or late async completions can’t leave
  the UI stuck or clobber user intent.
repository: aaif-goose/goose
label: Concurrency
language: TSX
comments_count: 2
repository_stars: 51876
---

When async flows drive UI state (events, config reads, resume/load), never assume timing/order will be favorable. Make initialization idempotent and conditionally applied so missed/early events or late async completions can’t leave the UI stuck or clobber user intent.

Apply these rules:
1) Provide a “catch-up” path for state that may already be loaded.
- If state depends on an event, also compute/load from current props/session immediately, so listener attachment timing can’t break visibility.
- Filter event handling by the relevant key (e.g., sessionId) and ignore mismatches.

2) Guard against out-of-order async updates.
- If an async read could complete after the user has interacted, only apply the persisted/async value when the user has not changed the control (or cancel/ignore stale work).

Example pattern (session event + immediate catch-up):
```ts
const loadForSession = (id: string) => {
  // load extensions for id (idempotent)
};

const onLoaded = (event: Event) => {
  const targetSessionId = (event as CustomEvent<{ sessionId?: string }>).detail?.sessionId;
  if (targetSessionId !== sessionId) return;
  loadForSession(targetSessionId!);
};

window.addEventListener(AppEvents.SESSION_EXTENSIONS_LOADED, onLoaded);
// catch-up: don’t rely solely on whether the event already fired
loadForSession(sessionId);
```

Example pattern (async config read without clobbering user choice):
```ts
let userTouched = false;

// set userTouched = true in your dropdown onChange

const effortFromConfig = await readConfig('SOME_EFFORT_KEY');
if (effortFromConfig && !userTouched) {
  setEffort(effortFromConfig);
}
```

Keep “ordering hazards” (e.g., user actions during resume vs backend load) scoped or explicitly disabled unless you can key off a reliable in-progress signal; otherwise treat them as separate follow-ups to avoid mixing multiple concurrency risks in one change.