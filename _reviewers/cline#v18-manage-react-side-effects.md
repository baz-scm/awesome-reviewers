---
title: Manage React Side Effects
description: 'When UI visibility changes (e.g., resume/reconnect), treat lifecycle
  as a first-class requirement: preserve user state, prevent unintended re-initialization,
  and use semantic JSX for reliable interaction.'
repository: cline/cline#v18
label: React
language: TSX
comments_count: 3
repository_stars: 70884
---

When UI visibility changes (e.g., resume/reconnect), treat lifecycle as a first-class requirement: preserve user state, prevent unintended re-initialization, and use semantic JSX for reliable interaction.

**Apply this standard**
1. **Prefer hide/show over unmount when state must persist.** If you temporarily hide a feature (startup screen, loading overlay), keep the component mounted and only toggle visibility so conversation/thread selection doesn’t reset. Also ensure hidden content releases focus traps and interaction locks while the overlay is active.
2. **Make effects resilient to resume/reconnect.** If an effect re-runs on reconnect/visibility changes, gate one-time “bootstrap” actions (navigation/selection dispatches) behind a stable ref so they run only after the first successful initialization, while allowing necessary refreshes to continue.
3. **Use semantic interactive elements in JSX.** Don’t rely on click handlers on non-interactive/incorrect elements. For controls, use `<button type="button">` (styled as needed) so keyboard activation works and tests can assert semantics.

**Pattern (one-time bootstrap, repeated refresh)**
```tsx
function useRemoteEnvironmentBootstrap() {
  const bootstrappedRef = React.useRef(false);

  React.useEffect(() => {
    let cancelled = false;

    async function run() {
      const ok = await initializeRemoteEnvironment();
      if (cancelled) return;

      // Always refresh active environment on each load
      dispatch(setActiveRemoteEnvironment(/* ... */));

      // But only do the one-time selection/navigation once
      if (ok && !bootstrappedRef.current) {
        bootstrappedRef.current = true;
        dispatch(selectEnvironmentDraft(/* first draft */));
      }
    }

    run();
    return () => { cancelled = true; };
  }, [/* reconnect-sensitive deps */]);
}

// For interactive UI:
<button type="button" onClick={handleChooseModel}>Choose model</button>
```