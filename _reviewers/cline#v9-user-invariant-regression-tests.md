---
title: User-Invariant Regression Tests
description: When fixing user-visible behavior, add reproduction-level regression
  tests that assert the specific user-facing invariant (not just the internal implementation).
  Cover cases where events or UI state transitions are sensitive to focus, mounts,
  and rendering timing.
repository: cline/cline#v9
label: Testing
language: TSX
comments_count: 2
repository_stars: 70868
---

When fixing user-visible behavior, add reproduction-level regression tests that assert the specific user-facing invariant (not just the internal implementation). Cover cases where events or UI state transitions are sensitive to focus, mounts, and rendering timing.

How to apply:
- Keyboard/event fixes: add an integration test that triggers the shortcut under realistic focus (e.g., on a textarea) and asserts the intended handler runs while the nested/input handler is not invoked.
- UI/layout fixes: add a desktop/integration regression test that loads the saved state and performs the same transition (e.g., optimistic/“Thinking…” swap). Assert the viewport/scroll position invariant (e.g., it stays near the newly pinned prompt; scrollTop must not jump to 0).
- Ensure the test would fail on the prior behavior (“unpatched dist”) and pass with the fix.

Example (event propagation invariant):
```ts
it("quit keydown on textarea never reaches textarea handler", async () => {
  renderAppWithWebview();
  focus("textarea");

  dispatchKeyDown({ key: "q", metaKey: true }); // quit accelerator

  expect(textareaHandler).not.toHaveBeenCalled();
  expect(quitAppInvoked).toHaveBeenCalled();
});
```

Example (viewport invariant):
```ts
it("saved transcript swap keeps the viewport anchored", async () => {
  loadSavedConversation({ prompts: 5 });
  pinNewPromptDuringSwap(); // simulate Thinking->first answer replacement

  expect(isNearPinnedPromptViewport()).toBe(true);
  expect(scrollTop()).not.toBe(0);
});
```