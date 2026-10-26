---
title: State-Preserving React UI
description: When UI depends on async readiness/reconnects, design components so state
  is preserved across transitions while still preventing focus/pointer-event traps
  and avoiding unintended re-initialization.
repository: Cline/Cline
label: React
language: TSX
comments_count: 4
repository_stars: 70840
---

When UI depends on async readiness/reconnects, design components so state is preserved across transitions while still preventing focus/pointer-event traps and avoiding unintended re-initialization.

Apply these rules:
1) Mount once; hide/show on recoverable states.
- If reconnect/retry should keep user context (selected conversation, open dialogs), don’t unmount the main app—hide it.
- Ensure hidden content releases focus traps and disables pointer events so the startup/placeholder UI is truly interactive.

2) Gate “bootstrap” effects separately from “refresh” effects.
- If an effect should run only after the first successful initialization, use a ref flag to track the first success.
- Keep per-reconnect refresh behavior separate from one-time navigation/selection logic.

3) Separate user intent from programmatic updates.
- For event-driven state (scroll pinning, selection changes), track whether the change was triggered by the user.
- Guard handlers based on event target so keyboard/mouse input inside focused child controls doesn’t trigger parent behavior.

Example pattern:
```tsx
function Home() {
  const startup = useHubStartup();
  const hubReady = startup.transport === 'connected' && startup.hub.state === 'ready';
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    if (hubReady) setMounted(true);
  }, [hubReady]);

  // Preserve App state, but disable interaction/focus while startup screen is active.
  return (
    <>
      {mounted ? (
        <Activity mode={hubReady ? 'visible' : 'hidden'}>
          <App />
        </Activity>
      ) : null}
      {!mounted || !hubReady ? <HubStartupScreen {...startup} /> : null}
    </>
  );
}

function useRemoteEnvironmentBootstrap(activeEnvId, firstSuccessAction) {
  const didBootstrapRef = useRef(false);
  useEffect(() => {
    if (!activeEnvId) return;
    if (!didBootstrapRef.current) {
      didBootstrapRef.current = true;
      firstSuccessAction(); // navigation/selection only once
    }
    // refresh other data on every successful load/reconnect
  }, [activeEnvId, firstSuccessAction]);
}
```

Use this standard to prevent: lost UI context on retries, focus traps behind placeholder screens, and accidental re-navigation/selection changes when hidden components re-show after reconnects.