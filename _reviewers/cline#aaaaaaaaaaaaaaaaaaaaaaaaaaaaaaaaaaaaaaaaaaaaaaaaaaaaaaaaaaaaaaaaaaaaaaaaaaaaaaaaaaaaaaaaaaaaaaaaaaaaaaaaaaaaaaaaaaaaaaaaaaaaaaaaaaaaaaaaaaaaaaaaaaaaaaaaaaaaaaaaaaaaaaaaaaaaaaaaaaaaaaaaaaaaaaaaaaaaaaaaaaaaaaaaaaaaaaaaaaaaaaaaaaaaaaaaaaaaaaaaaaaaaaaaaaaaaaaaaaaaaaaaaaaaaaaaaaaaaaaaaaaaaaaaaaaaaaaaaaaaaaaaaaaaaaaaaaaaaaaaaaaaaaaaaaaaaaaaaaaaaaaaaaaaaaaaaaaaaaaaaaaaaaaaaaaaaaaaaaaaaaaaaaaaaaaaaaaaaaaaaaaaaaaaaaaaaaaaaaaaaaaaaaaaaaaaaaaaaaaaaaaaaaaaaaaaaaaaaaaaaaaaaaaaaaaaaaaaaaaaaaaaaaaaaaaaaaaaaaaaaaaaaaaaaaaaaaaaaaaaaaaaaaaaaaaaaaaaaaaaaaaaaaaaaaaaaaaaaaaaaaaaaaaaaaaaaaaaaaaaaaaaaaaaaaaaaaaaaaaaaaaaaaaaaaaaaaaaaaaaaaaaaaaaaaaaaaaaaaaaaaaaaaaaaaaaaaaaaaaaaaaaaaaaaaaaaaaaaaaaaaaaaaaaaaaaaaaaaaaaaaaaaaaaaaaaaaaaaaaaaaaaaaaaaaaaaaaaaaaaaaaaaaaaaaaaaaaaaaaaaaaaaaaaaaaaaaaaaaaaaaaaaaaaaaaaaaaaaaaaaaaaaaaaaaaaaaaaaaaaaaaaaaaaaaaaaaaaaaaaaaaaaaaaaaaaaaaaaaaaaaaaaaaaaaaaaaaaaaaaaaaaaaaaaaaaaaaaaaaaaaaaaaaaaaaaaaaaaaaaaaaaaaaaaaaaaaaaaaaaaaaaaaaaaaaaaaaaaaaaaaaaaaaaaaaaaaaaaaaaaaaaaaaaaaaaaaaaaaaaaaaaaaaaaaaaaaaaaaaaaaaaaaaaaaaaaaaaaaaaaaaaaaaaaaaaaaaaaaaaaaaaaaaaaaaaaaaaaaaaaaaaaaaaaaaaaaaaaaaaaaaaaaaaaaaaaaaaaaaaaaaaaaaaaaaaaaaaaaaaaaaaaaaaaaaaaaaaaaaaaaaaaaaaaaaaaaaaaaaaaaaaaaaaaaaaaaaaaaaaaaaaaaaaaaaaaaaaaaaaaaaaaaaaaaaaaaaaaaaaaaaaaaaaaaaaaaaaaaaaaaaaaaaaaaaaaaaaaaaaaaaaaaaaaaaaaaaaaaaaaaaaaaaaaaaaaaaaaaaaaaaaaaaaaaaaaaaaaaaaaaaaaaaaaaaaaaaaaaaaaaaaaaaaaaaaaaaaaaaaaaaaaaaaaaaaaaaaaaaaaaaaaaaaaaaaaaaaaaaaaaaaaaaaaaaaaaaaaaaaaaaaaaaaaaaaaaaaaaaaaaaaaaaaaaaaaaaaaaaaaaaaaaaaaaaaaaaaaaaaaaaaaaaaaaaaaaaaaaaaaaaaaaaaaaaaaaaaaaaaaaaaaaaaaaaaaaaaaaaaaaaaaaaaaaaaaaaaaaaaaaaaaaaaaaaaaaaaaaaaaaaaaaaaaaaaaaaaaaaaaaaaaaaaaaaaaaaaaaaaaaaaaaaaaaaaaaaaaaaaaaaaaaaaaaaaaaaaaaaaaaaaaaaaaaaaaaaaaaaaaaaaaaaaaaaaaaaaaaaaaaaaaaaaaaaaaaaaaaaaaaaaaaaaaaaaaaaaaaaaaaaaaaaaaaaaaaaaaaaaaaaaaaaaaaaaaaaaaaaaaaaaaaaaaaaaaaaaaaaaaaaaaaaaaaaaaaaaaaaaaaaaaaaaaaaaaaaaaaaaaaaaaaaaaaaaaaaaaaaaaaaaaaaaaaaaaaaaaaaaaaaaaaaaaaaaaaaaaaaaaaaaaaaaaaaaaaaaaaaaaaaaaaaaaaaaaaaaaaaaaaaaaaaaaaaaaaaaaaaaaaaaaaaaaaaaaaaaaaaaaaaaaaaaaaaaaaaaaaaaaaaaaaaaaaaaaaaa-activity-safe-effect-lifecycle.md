---
title: Activity-safe effect lifecycle
description: 'When a subtree is hidden instead of unmounted (e.g. wrapped in `<Activity
  mode="hidden">`, or toggled behind a covering overlay) to preserve component state
  like open conversations, its effects still tear down and rerun on every visibility
  change. Design effects in such subtrees with this in mind:'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: React
language: TSX
comments_count: 3
repository_stars: 70976
---

When a subtree is hidden instead of unmounted (e.g. wrapped in `<Activity mode="hidden">`, or toggled behind a covering overlay) to preserve component state like open conversations, its effects still tear down and rerun on every visibility change. Design effects in such subtrees with this in mind:

1. **"Run once" bootstrap effects must survive hide/show cycles.** A `useState`-backed "has this run" flag resets to its initial value on remount, but a `useRef` flag does not reset when Activity hides and re-shows the tree. If an effect should only perform its one-time side effect (e.g. dispatching an initial navigation) on the very first successful run, gate it with a ref, not state, and make sure the ref is only set after success (a failed/cancelled attempt should not block a future retry):

```tsx
const bootstrappedRef = useRef(false);
useEffect(() => {
  loadContext().then((ctx) => {
    refreshEnvironment(ctx); // safe to repeat on every visible cycle
    if (!bootstrappedRef.current) {
      bootstrappedRef.current = true;
      dispatch({ type: "select-environment-draft", ctx }); // only once, ever
    }
  });
}, [/* deps that should refresh, e.g. reconnects */]);
```

2. **Unmount-only cleanup must still reset state that Activity keeps alive.** A cleanup function that assumes "unmounting means the component is gone" can leave derived state (e.g. `isListening`, `isProcessing`) stuck in a stale "active" value when the component is hidden mid-operation and shown again, because that state is preserved across the hide/show instead of reset. Cancel the operation *and* reset all state the UI depends on in the cleanup, even though doing so is a no-op on a true unmount:

```tsx
useEffect(() => {
  return () => {
    cancelRecording();
    setIsListening(false);
    setIsProcessing(false);
    onActiveChange(false);
  };
}, []);
```

3. **Prefer hiding over covering when a dialog-bearing subtree needs to be temporarily disabled.** Covering one tree with another (e.g. an error/startup screen rendered on top of the app) can leave the covered tree's dialogs mounted, trapping focus or disabling body pointer events even though they're invisible. Swapping the tree out (conditional render) or hiding it via `Activity` ensures its effects — and any focus traps or portals they created — are properly torn down.

Whenever you introduce a pattern that keeps a subtree's state alive while hiding it, audit every effect in that subtree for implicit "this only happens once" or "this only happens on unmount" assumptions, and add a regression test that drives the component through hide → show (or busy → idle → busy) and asserts state didn't leak or reset incorrectly.