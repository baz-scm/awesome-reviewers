---
title: Visibility-safe React state
description: When building React UIs that can be hidden/shown (startup screens, side
  panels, modals, drawers, activity shells), design for **correct state + correct
  side effects** across transitions.
repository: ClInE/cLiNe
label: React
language: TSX
comments_count: 6
repository_stars: 70838
---

When building React UIs that can be hidden/shown (startup screens, side panels, modals, drawers, activity shells), design for **correct state + correct side effects** across transitions.

**Rules**
1) **Preserve state when possible:** If the user should keep their current context (selected conversation/session, drafts, etc.), prefer keeping the component mounted and switching to a hidden/visible mode rather than unmounting.
2) **But manage side effects explicitly on hide:** Hidden mode should reliably:
   - cancel/cleanup in-flight processes or timers
   - tear down effects that create focus traps or intercept input
   - release `pointer-events`/focus affordances so the overlay/screen is the only interactive surface.
3) **Guard one-time bootstraps:** If a hook both (a) refreshes on every reconnect and (b) performs a one-time navigation/selection change, split those responsibilities or guard the one-time part with a ref.
4) **Handle event intent precisely:** For custom scroll/resize/selection behaviors, track whether changes are caused by the user or by your own programmatic calls; only user input should unpin/unfocus/etc. Also ensure keyboard handlers don’t steal input from focused child controls.
5) **Make custom controls accessible:** For interactive non-native UI (resize handles, sliders), use the right ARIA role/attributes and keyboard controls (e.g., role="separator" + arrow key resizing).

**Example pattern (hidden vs one-time bootstrap)**
```tsx
function Page() {
  const [loaded, setLoaded] = useState(false);
  const startup = useHubStartup();
  const hubReady = startup.transport === 'connected' && startup.hub.state === 'ready';
  const hubFailed = startup.transport === 'connected' && startup.hub.state === 'failed';

  useEffect(() => {
    if (hubReady) setLoaded(true);
  }, [hubReady]);

  return (
    loaded ? (
      <Activity mode={hubReady ? 'visible' : 'hidden'}>
        <App />
      </Activity>
    ) : (
      <HubStartupScreen {...startup} />
    )
  );
}

function useRemoteEnvironmentBootstrap() {
  const didBootstrapRef = useRef(false);

  useEffect(() => {
    if (!didBootstrapRef.current) {
      didBootstrapRef.current = true;
      // one-time selection/navigation bootstrap
    }
    // always refresh active environment on reconnect
  }, [/* reconnect state */]);
}
```

**Checklist to apply in reviews**
- Does hidden mode preserve the needed UI state?
- Are effects cleaned/canceled when hidden so focus/pointer aren’t trapped?
- Is any “first-load” navigation/selection guarded against repeated show/hide cycles?
- Do event handlers clearly separate user vs programmatic changes?
- Are keyboard/ARIA requirements met for custom controls?