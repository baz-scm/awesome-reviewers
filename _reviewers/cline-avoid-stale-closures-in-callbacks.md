---
title: Avoid stale closures in callbacks
description: When an effect, timer, or async operation schedules a callback that may
  run after a gap (an `await`, an interval tick, or a React `<Activity>` hide/show
  cycle), do not let it act on values captured in its closure at creation time — state
  may have changed by the time it fires. Read the current value through a ref that
  is kept up to date on every render/call,...
repository: cline/cline
label: React
language: TSX
comments_count: 5
repository_stars: 70886
---

When an effect, timer, or async operation schedules a callback that may run after a gap (an `await`, an interval tick, or a React `<Activity>` hide/show cycle), do not let it act on values captured in its closure at creation time — state may have changed by the time it fires. Read the current value through a ref that is kept up to date on every render/call, or gate the behavior on a ref-backed flag, since refs (unlike state) survive effect teardown from `<Activity>` hiding and are always current when the callback finally runs.

Example pattern: a reload function triggered after an async action (e.g. a git pull) must use the up-to-date set of expanded folders, not the set that existed when the callback was created:

```tsx
const expandedRef = useRef(expanded);
expandedRef.current = expanded;

const reloadDirectories = useCallback(() => {
  const open = expandedRef.current; // current, not stale
  // ...reload using `open`
}, [loadDirectory]);
```

The same pattern applies to:
- "run once" bootstrap effects that must not re-fire when `<Activity>` remounts effects on resume — track completion in a ref, not state, so the flag survives hiding.
- timer/flush refs cleared on unmount — explicitly null them in cleanup so a later remount (e.g. after `<Activity>` becomes visible again) re-arms the scheduler instead of silently no-oping.
- refresh keys derived from aggregated/summary data (e.g. accumulated diff totals) that only change at coarse boundaries — key off the more granular signal that actually changes (e.g. a per-event count) so updates aren't missed between boundaries.

Before merging logic that reads stale-prone values in a deferred callback, ask: "could this callback fire after the state it closed over has moved on?" If yes, back it with a ref and add a test that exercises the race (state changes while the async/deferred operation is in flight).