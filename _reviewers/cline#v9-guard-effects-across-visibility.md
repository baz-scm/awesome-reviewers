---
title: Guard effects across visibility
description: 'When React components are hidden/shown (e.g., via an <Activity> wrapper)
  or temporarily enter an exclusive UI mode (startup/recording), assume effects and
  event handlers may re-run or still be “listening”. To prevent user-state regressions
  and interaction conflicts, follow these rules:'
repository: cline/cline#v9
label: React
language: TSX
comments_count: 5
repository_stars: 70868
---

When React components are hidden/shown (e.g., via an <Activity> wrapper) or temporarily enter an exclusive UI mode (startup/recording), assume effects and event handlers may re-run or still be “listening”. To prevent user-state regressions and interaction conflicts, follow these rules:

- Treat initialization as *explicitly one-time*: move “bootstrap/navigation” logic into a dedicated hook and gate it with a ref (e.g., run only after the first successful init). Still allow required refreshes on reconnect.
- Preserve intent across visibility toggles: if state matters (active conversation, scroll pin), store ownership/flags in refs so hiding/showing doesn’t reset behavioral rules.
- Separate programmatic vs user actions: for scroll/keyboard handling, only unpin or change pinned state based on direct user intent (wheel/keys), not on the resulting async scroll events from your own code.
- Isolate exclusive modes: when entering a mode like shortcut recording or showing a startup overlay, suspend competing listeners (and/or add a shared “isSuspended” flag) so other handlers don’t interfere; ensure event propagation is blocked when necessary.
- Add targeted tests for hide/show + reconnect and for interaction edge cases (e.g., remote conversation selection across visible→hidden→visible; scroll restore until scrollHeight is sufficient).

Example: “one-time bootstrap with ref guard”

```ts
function useRemoteEnvironmentBootstrap({ initialized, dispatch, selectDraft }) {
  const didBootstrapRef = React.useRef(false);

  React.useEffect(() => {
    if (!initialized) return;

    // Always refresh environment data on every successful init/reconnect.
    dispatch({ type: "refreshActiveRemoteEnvironment" });

    // Only do one-time navigation/selection bootstrap once.
    if (!didBootstrapRef.current) {
      didBootstrapRef.current = true;
      selectDraft();
    }
  }, [initialized, dispatch, selectDraft]);
}
```

Apply this pattern to any effect that must not re-run due to visibility changes, and pair it with explicit ownership rules for user vs programmatic interactions (scroll, keyboard, recording handlers).