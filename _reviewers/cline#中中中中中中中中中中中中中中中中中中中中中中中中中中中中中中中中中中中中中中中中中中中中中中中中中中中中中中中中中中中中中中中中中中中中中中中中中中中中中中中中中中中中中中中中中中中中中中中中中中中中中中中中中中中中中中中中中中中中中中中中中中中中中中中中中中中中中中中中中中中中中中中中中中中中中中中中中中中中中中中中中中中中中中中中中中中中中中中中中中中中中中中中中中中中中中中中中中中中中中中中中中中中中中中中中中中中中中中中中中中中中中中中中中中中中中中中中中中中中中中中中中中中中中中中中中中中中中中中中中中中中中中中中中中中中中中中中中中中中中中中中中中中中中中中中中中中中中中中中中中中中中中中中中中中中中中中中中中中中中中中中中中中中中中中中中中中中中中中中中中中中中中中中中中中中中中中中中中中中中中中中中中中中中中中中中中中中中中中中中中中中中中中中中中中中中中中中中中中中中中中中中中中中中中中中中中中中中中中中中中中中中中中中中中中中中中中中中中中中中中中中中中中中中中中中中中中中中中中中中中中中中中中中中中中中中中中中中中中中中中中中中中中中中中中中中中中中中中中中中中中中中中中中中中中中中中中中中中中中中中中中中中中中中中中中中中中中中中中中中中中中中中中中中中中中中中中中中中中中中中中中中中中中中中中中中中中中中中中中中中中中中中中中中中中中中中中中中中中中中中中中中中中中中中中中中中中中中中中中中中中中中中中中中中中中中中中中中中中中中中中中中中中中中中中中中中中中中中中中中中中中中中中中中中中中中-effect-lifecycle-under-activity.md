---
title: Effect lifecycle under Activity
description: 'When a subtree is hidden instead of unmounted (React''s `<Activity>`,
  or any conditional-render-but-keep-state pattern), effects are torn down on hide
  and rerun on show — this is not a true unmount/mount cycle, so code must not assume
  otherwise. Two concrete rules follow: (1) any "run only once" initialization (e.g.
  bootstrapping navigation/state from a...'
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: React
language: TSX
comments_count: 5
repository_stars: 70986
---

When a subtree is hidden instead of unmounted (React's `<Activity>`, or any conditional-render-but-keep-state pattern), effects are torn down on hide and rerun on show — this is not a true unmount/mount cycle, so code must not assume otherwise. Two concrete rules follow: (1) any "run only once" initialization (e.g. bootstrapping navigation/state from a one-time load) must be gated by a `ref`, not component mount, since refs are the only thing guaranteed to persist across a hide/show cycle while state recreated in render or effect state is not reliably safe to lean on for this; every rerun should still refresh truly current data (e.g. re-fetching environment/process context) but only the gated action (e.g. dispatching an initial navigation) should fire once. (2) effect cleanup functions must fully reset any external or imperative side effect (timers, recording flags, subscriptions) exactly as they would on a genuine unmount, because that cleanup now also runs on every hide — a cleanup that only cancels the underlying operation but leaves local "isListening"/"isProcessing" state stale will desync the UI when the component becomes visible again. Treat hide/show as a lighter-weight lifecycle than mount/unmount, but verify with explicit tests (hide the tree mid-operation, show it again, assert state is consistent) rather than assuming existing unmount-based cleanup is sufficient.

```tsx
function useRemoteEnvironmentBootstrap() {
  const bootstrappedRef = useRef(false); // survives Activity hiding
  useEffect(() => {
    getProcessContext().then((ctx) => {
      refreshActiveEnvironment(ctx); // always refresh on every run
      if (!bootstrappedRef.current) {
        bootstrappedRef.current = true;
        dispatch(selectEnvironmentDraft(ctx)); // navigate only once, ever
      }
    });
  }, []);
}

function SpeechInput() {
  useEffect(() => {
    return () => {
      // Runs on hide too, not just unmount: must fully reset state,
      // not just stop the side effect.
      cancelRecording();
      setIsListening(false);
      setIsProcessing(false);
    };
  }, []);
}
```