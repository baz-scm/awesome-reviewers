---
title: Lifecycle-safe hide/show components
description: 'When a component is hidden instead of unmounted (e.g. wrapped in React''s
  `<Activity>`, or kept alive behind a loading/error overlay) to preserve its state,
  its effects still run their cleanup on hide and re-run on show. Two rules follow
  from this:'
repository: cline/cline#|sleep 4
label: React
language: TSX
comments_count: 4
repository_stars: 70979
---

When a component is hidden instead of unmounted (e.g. wrapped in React's `<Activity>`, or kept alive behind a loading/error overlay) to preserve its state, its effects still run their cleanup on hide and re-run on show. Two rules follow from this:

1. **Effect cleanups must fully reset any side-effect-driven state**, not just cancel the underlying operation. If an effect starts a recording/stream/timer and sets state like `isListening`, its cleanup must also reset that state (and notify any callback that depends on it), otherwise the component resurfaces in a stale "still active" UI state even though the real operation was cancelled.

```tsx
useEffect(() => {
  if (!isListening) return;
  const session = startRecording();
  return () => {
    session.cancel();
    // Don't just stop the side effect — reset the state that drove it,
    // so re-showing the component reflects reality.
    setIsListening(false);
    setIsProcessing(false);
    onActiveChange(false);
  };
}, [isListening]);
```

2. **Use a `ref`, not `state`, to guard "run once" initialization logic that must survive a hide/show cycle.** Refs persist across hide/show (and StrictMode remounts) while effects re-run; relying on an effect's local closure or re-running an initial-bootstrap dispatch on every show will incorrectly reset derived UI (e.g. navigating back to a draft/blank view) on reconnect. Split "run always" logic (e.g. refreshing data) from "run once" logic (e.g. initial navigation) explicitly:

```tsx
const hasBootstrapped = useRef(false);

useEffect(() => {
  loadContext().then((context) => {
    refreshEnvironment(context); // always refresh
    if (!hasBootstrapped.current) {
      hasBootstrapped.current = true;
      dispatch({ type: "select-initial-draft" }); // only once, ever
    }
  });
}, []);
```

Before introducing any hide/show-instead-of-unmount pattern, audit every effect in the subtree for (a) state that needs resetting on cleanup and (b) one-time logic that must be guarded with a ref rather than re-triggered on remount/reshow. Add a test that drives the component through hide → show (or the equivalent reconnect/retry path) and asserts both the side-effect state and the one-time logic behave correctly.