---
title: User-intent state transitions
description: In React components, ensure state changes are driven by (a) the correct
  lifecycle moment and (b) the correct source of the triggering event—not by incidental
  visibility toggles or programmatic updates. Also avoid over-sharing derived/identity-specific
  values in shared context.
repository: cline/cline#v27
label: React
language: TSX
comments_count: 4
repository_stars: 70892
---

In React components, ensure state changes are driven by (a) the correct lifecycle moment and (b) the correct source of the triggering event—not by incidental visibility toggles or programmatic updates. Also avoid over-sharing derived/identity-specific values in shared context.

Apply this as a standard:
1) Scope state/data to its owner
- Put stable, app-wide configuration (e.g., environment base URLs) in shared context.
- Keep account-specific or derived links/actions inside the owning view/component; don’t broadcast identity-derived values solely to support UI duplication.

2) Choose mount vs hide intentionally
- If you must preserve user selection/state across hub/connectivity changes, prefer “hide” (e.g., an Activity-like wrapper) over “unmount”, but ensure hidden content releases side effects (focus traps, portaled dialogs, pointer-events).
- If the UI state would become inconsistent or controls would conflict, replace/unmount on failure.

3) Make effects idempotent with explicit “one-time after successful init” guards
- When components can be hidden/shown, don’t re-run one-time bootstrap/navigation on every re-render/visibility change.
- Use a ref (or equivalent) to mark “first successful load completed” and only then allow one-time dispatches; still refresh dependent data on reconnect.

4) Separate user-driven vs programmatic events
- For scroll/pinned UI, track the “programmatic scroll target” and ignore scroll events that are a side effect of your own scrolling.
- Only un-pin on genuine user input (wheel/arrow keys aimed at the viewport/reader intent), not on your own scroll operations.

Example (pattern for “one-time after successful init” + visibility):
```tsx
function useRemoteBootstrap(visibility: boolean) {
  const hasBootstrappedRef = useRef(false);

  useEffect(() => {
    if (!visibility) return;

    let cancelled = false;
    async function run() {
      const ok = await initializeRemoteEnvironment(); // success/fail
      if (cancelled) return;

      refreshActiveEnvironment(); // per reconnect
      if (ok && !hasBootstrappedRef.current) {
        hasBootstrappedRef.current = true;
        dispatchSelectInitialDraftOnce();
      }
    }
    run();
    return () => { cancelled = true; };
  }, [visibility]);
}
```

Example (pattern for scroll/pin origin tracking):
```tsx
const ourScrollTarget = useRef<number | null>(null);

const scrollToBottom = () => {
  setPinned(true);
  ourScrollTarget.current = viewport.scrollHeight;
  viewport.scrollTo({ top: viewport.scrollHeight, behavior: 'smooth' });
};

const onScroll = () => {
  if (ourScrollTarget.current !== null) {
    const arrived = Math.abs(viewport.scrollTop - ourScrollTarget.current) <= 1;
    if (arrived) ourScrollTarget.current = null;
    else return; // ignore in-flight programmatic scroll events
  }
  // user-driven scroll updates pinned state
};
```

Result: fewer state sync bugs, preserved user context across connectivity/visibility changes, and UI behavior that matches user intent rather than internal updates.