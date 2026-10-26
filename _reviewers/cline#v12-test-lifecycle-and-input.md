---
title: Test Lifecycle and Input
description: 'Add integration/behavior tests for UI behaviors that depend on DOM focus,
  event propagation, and lifecycle transitions.


  **When changing keyboard/event handling**'
repository: cline/cline#v12
label: Testing
language: TSX
comments_count: 2
repository_stars: 70872
---

Add integration/behavior tests for UI behaviors that depend on DOM focus, event propagation, and lifecycle transitions.

**When changing keyboard/event handling**
- Prove the event is routed correctly in the real target context (e.g., textarea/contenteditable should not receive the shortcut).
- Assert “not reached” behavior with a DOM-context test.

**When changing initialization/bootstrapping tied to visibility, reconnect, or mount/unmount**
- Use a realistic harness (e.g., render the real container such as `Activity` plus the app reducer/store) and simulate the full lifecycle transition sequence (visible → hidden → visible).
- Assert user-critical state remains stable (e.g., active remote conversation/thread selection) and that bootstrap logic runs the intended number of times.
- Include at least one failure/cancellation path followed by a successful retry, so “initialization that didn’t land” doesn’t incorrectly block later bootstraps.

**Example pattern (integration assertions)**
```ts
it("preserves selection across Activity hide/show", async () => {
  const { store, getByRole } = renderWithDesktopReducerAndActivity();

  // Open a remote draft/thread
  await act(async () => {
    await openSshDraftAndStartThread(store);
  });
  expect(store.getState().activeThreadId).toBe("draft-1");

  // Simulate lifecycle transition that unmounts effects
  await act(async () => {
    rerender(<Activity mode="hidden" />);
    rerender(<Activity mode="visible" />);
  });

  // Assert the critical state is preserved
  expect(store.getState().activeThreadId).toBe("draft-1");
  // Optionally assert bootstrap executed the expected times
  expect(get_process_context).toHaveBeenCalledTimes(2);
});
```

This ensures subtle regressions from focus/shortcut propagation and effect re-runs during lifecycle changes are caught before release.