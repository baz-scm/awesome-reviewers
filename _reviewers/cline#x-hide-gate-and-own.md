---
title: Hide, gate, and own
description: For React UIs driven by async readiness/reconnect (or other multi-phase
  state), preserve user state and avoid unintended side effects by (1) preferring
  hiding over unmounting when you need continuity, (2) gating one-time initialization
  separately from refresh logic, and (3) ensuring input/event handling and interactive
  semantics are owned by the correct...
repository: cline/cline#x
label: React
language: TSX
comments_count: 4
repository_stars: 70861
---

For React UIs driven by async readiness/reconnect (or other multi-phase state), preserve user state and avoid unintended side effects by (1) preferring hiding over unmounting when you need continuity, (2) gating one-time initialization separately from refresh logic, and (3) ensuring input/event handling and interactive semantics are owned by the correct user intent (with accessibility-correct elements).

How to apply:
- Preserve continuity: if the user’s context (threads, selections, forms) must survive a readiness transition, keep the component mounted and hide it (e.g., via a visibility prop or container styling) rather than unmounting/remounting.
- Release UX constraints: when hidden, ensure focus traps, pointer-events, and portaled overlays don’t block interaction with the active startup/placeholder UI.
- Gate effects: separate “run once after first successful init” from “refresh on every reconnect.” Use a ref/flag so effects don’t re-dispatch navigation/bootstrap actions on later hide/show cycles.

Example pattern:
```tsx
function ScreenOrApp({ ready, getProcessContext }) {
  const [loaded, setLoaded] = useState(false);
  const firstSuccessRef = useRef(false);

  useEffect(() => {
    if (ready) setLoaded(true);
  }, [ready]);

  useEffect(() => {
    if (!loaded || !ready) return;
    // Always refresh context
    getProcessContext();
    // But only bootstrap navigation/selection once
    if (!firstSuccessRef.current) {
      firstSuccessRef.current = true;
      // dispatch(select-environment-draft) or similar
    }
  }, [loaded, ready, getProcessContext]);

  return (
    <>
      {loaded ? (
        <Activity mode={ready ? "visible" : "hidden"}>
          <App />
        </Activity>
      ) : null}
      {!ready ? <HubStartupScreen /> : null}
    </>
  );
}
```

- Own input correctly: when implementing state machines (e.g., “pinned to bottom”), distinguish programmatic actions from user intent and only un-pin on events from the appropriate target (don’t react to keypresses meant for focused child controls).
- Use accessible semantics: prefer native interactive elements (e.g., `<button type="button">`) for keyboard/assistive compatibility, and ensure tests assert the real semantics (not just styling).
- Test the tricky paths: add coverage for hide/show transitions and “open state” scenarios so regressions (like selection changes or accidental unpinning) are caught.