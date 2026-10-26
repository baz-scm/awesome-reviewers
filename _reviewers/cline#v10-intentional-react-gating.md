---
title: Intentional React gating
description: 'When UI behavior depends on async readiness (Hub transport/state, streams,
  etc.), don’t rely on naive mount/unmount or simple overlays. Instead:


  - **Choose rendering strategy intentionally:**'
repository: cline/cline#v10
label: React
language: TSX
comments_count: 5
repository_stars: 70869
---

When UI behavior depends on async readiness (Hub transport/state, streams, etc.), don’t rely on naive mount/unmount or simple overlays. Instead:

- **Choose rendering strategy intentionally:**
  - **Replace** the app with the startup screen when you must guarantee no mounted dialogs/popovers can trap focus or keep pointer events disabled.
  - Or **keep app state** but **hide with an Activity-style wrapper** so hidden content releases side effects (focus traps/portals/body pointer-events) while preserving user data.
- **Make effect lifecycles explicit:**
  - Split “first successful bootstrap” from “refresh on reconnect.” Use refs/guards so initialization runs once after the first successful ready state, while later reconnects still refresh the necessary derived data.
  - Add tests that cover **visible → hidden → visible** transitions and reconnection paths to prevent state drift (e.g., selected thread/environment).
- **Encode user intent vs programmatic effects:**
  - For event-driven state (scroll pinning, typing/keys), model whether the change came from **user input** or **programmatic calls**. Update “pinned/unpinned” state based on input (wheel/keys/reader actions), not on incidental scroll events produced by your own code.
  - Guard handlers so keyboard/mouse events that originate from focused child controls don’t trigger the parent’s state changes.

Example pattern (Activity gating + one-time bootstrap):
```tsx
function Home() {
  const startup = useHubStartup();
  const hubReady = startup.transport === "connected" && startup.hub.state === "ready";
  const [loaded, setLoaded] = useState(false);
  useEffect(() => {
    if (hubReady) setLoaded(true);
  }, [hubReady]);

  // Replace if you need to prevent any mounted focus traps
  const hubFailed = startup.transport === "connected" && startup.hub.state === "failed";

  return (
    <>
      {loaded && !hubFailed ? (
        <Activity mode={hubReady ? "visible" : "hidden"}>
          <App />
        </Activity>
      ) : null}
      {(!loaded || hubFailed) && <HubStartupScreen {...startup} />}
    </>
  );
}

function useRemoteEnvironmentBootstrap({ /* ... */ }) {
  const firstSuccessRef = useRef(false);

  useEffect(() => {
    let cancelled = false;
    async function run() {
      const ok = await init();
      if (cancelled || !ok) return;
      if (!firstSuccessRef.current) {
        firstSuccessRef.current = true;
        dispatch(selectEnvironmentDraft());
      }
      dispatch(refreshActiveEnvironment());
    }
    run();
    return () => { cancelled = true; };
  }, [/* reconnect deps */]);
}
```

Adopting this standard prevents the most common React UI bugs from these discussions: focus/pointer traps when overlays fail, lost user state after reconnect/hide, repeated initialization that mutates selection, and scroll/key interactions where programmatic updates accidentally overwrite user intent.