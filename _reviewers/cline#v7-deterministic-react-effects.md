---
title: Deterministic React Effects
description: In stateful React UIs, avoid “accidental remount/remodel” and unintended
  side effects caused by lifecycle timing. Use visibility toggles instead of unmounting
  when you must preserve state, and make effects run only when intended.
repository: cline/cline#v7
label: React
language: TSX
comments_count: 5
repository_stars: 70865
---

In stateful React UIs, avoid “accidental remount/remodel” and unintended side effects caused by lifecycle timing. Use visibility toggles instead of unmounting when you must preserve state, and make effects run only when intended.

Apply these rules:
- Preserve state across “hidden/shown” transitions: if you need to release focus traps/body pointer-events during startup/overlays, prefer rendering <App /> once and switching visibility (e.g., Activity mode) rather than unmounting.
- Make one-time vs repeat logic explicit:
  - Use refs/guards to ensure initialization (e.g., remote bootstrap, environment selection, first restore) happens only after the first successful condition.
  - Allow refresh logic to run on reconnect/updates without re-triggering one-time actions.
- Model event-driven UI intent explicitly:
  - Separate programmatic actions from user input (e.g., scroll-to-bottom vs reader scroll; shortcut recorder vs global handlers). Use refs to track “our target”/“suspension active” so scroll/keydown events don’t get misclassified.
- Scope and clean up side effects:
  - Suspend or stop propagation of global/page listeners during transient interaction modes.
  - Clean up observers/listeners deterministically in effect cleanups.

Example pattern (bootstrap runs once, refresh runs always; state preserved during hidden):
```tsx
function useRemoteBootstrap() {
  const firstSuccessRef = useRef(false);
  return (isReady: boolean) => {
    if (!isReady) return;
    // Always refresh needed state
    refreshActiveRemoteEnvironment();
    // But one-time navigation/selection only once
    if (!firstSuccessRef.current) {
      firstSuccessRef.current = true;
      dispatch(selectEnvironmentDraft());
    }
  };
}

export function Page() {
  const [visible, setVisible] = useState(false);
  const bootstrap = useRemoteBootstrap();
  useEffect(() => {
    bootstrap(visible);
  }, [visible, bootstrap]);

  return (
    <Activity mode={visible ? "visible" : "hidden"}>
      <App />
    </Activity>
  );
}
```
This standard prevents state loss (remount), focus trap regressions, and hard-to-debug race conditions caused by effect timing and event misclassification.