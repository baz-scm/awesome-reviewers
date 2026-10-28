---
title: Activity lifecycle effects
description: 'When a component is kept mounted but hidden instead of destroyed (e.g.
  React''s `<Activity>`, or a custom show/hide wrapper used to preserve state like
  an open conversation or selection across reconnects), its effects unmount and remount
  on every hide/show transition even though the component instance and its state never
  go away. Two bugs recur from this:'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: React
language: TSX
comments_count: 4
repository_stars: 70968
---

When a component is kept mounted but hidden instead of destroyed (e.g. React's `<Activity>`, or a custom show/hide wrapper used to preserve state like an open conversation or selection across reconnects), its effects unmount and remount on every hide/show transition even though the component instance and its state never go away. Two bugs recur from this:

1. **Cleanup must fully reset side-effect state, not just run on "real" unmount.** A cleanup that stops a side effect (e.g. cancels a recording) but leaves derived state flags (`isListening`, `isProcessing`) untouched will leave those flags stale when the component reappears, because the next mount's effect doesn't know the flags were never cleared. Reset all related state inside the cleanup itself so it's correct whether the unmount is permanent or just a hide:

```tsx
useEffect(() => {
  return () => {
    cancelRecording();
    setIsListening(false); // not just on "true" unmount
    setIsProcessing(false);
  };
}, []);
```

2. **Guard "run once" effects with a ref, not a plain mount effect.** Bootstrap/navigation effects that must fire only on the component's first successful initialization (not on every reactivation after a hide/show cycle) need a ref flag, since refs — unlike effect-local closures — survive the hide. Only flip the ref after the operation actually succeeds, so a failed or cancelled attempt still lets the next mount try the one-time action:

```tsx
const bootstrappedRef = useRef(false);
useEffect(() => {
  loadContext().then((result) => {
    refreshSomethingThatShouldAlwaysRun(result);
    if (!bootstrappedRef.current) {
      bootstrappedRef.current = true;
      dispatchOneTimeNavigation(result);
    }
  });
}, [dependency]);
```

When introducing or reviewing a hide-instead-of-unmount pattern, explicitly test the hide → show → hide → show cycle (including a failed attempt before a successful one) to confirm state is preserved where intended and reset where intended, and that effects with side effects on focus, portals, or external resources (dialogs, speech/recording sessions, timers) release and reacquire correctly.