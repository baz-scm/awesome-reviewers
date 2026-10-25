---
title: Test Shortcut Propagation
description: 'Add targeted tests whenever keyboard shortcut logic changes to prevent
  accidental shortcut/event leakage.


  Requirements:

  - Verify shortcut suspension lifecycle: if your code uses a suspension mechanism
  (e.g., `suspendShortcuts()` + `areShortcutsSuspended()`), include a unit test that
  proves shortcuts remain inactive until *all* suspensions are released.'
repository: cline/CLINE
label: Testing
language: TSX
comments_count: 2
repository_stars: 70839
---

Add targeted tests whenever keyboard shortcut logic changes to prevent accidental shortcut/event leakage.

Requirements:
- Verify shortcut suspension lifecycle: if your code uses a suspension mechanism (e.g., `suspendShortcuts()` + `areShortcutsSuspended()`), include a unit test that proves shortcuts remain inactive until *all* suspensions are released.
- Verify DOM event routing: if a matched keydown should only be handled by the shortcut layer, add a test that the keydown does **not** reach other UI handlers (e.g., textarea/chat input), reflecting the implementation detail that uses `stopImmediatePropagation()`.

Example test assertions (shape):
```ts
// 1) suspension lifecycle
expect(areShortcutsSuspended()).toBe(true);
// simulate keydown(s) that would normally trigger shortcut
// assert handlers were not called

// 2) propagation isolation
// render textarea/chat input with its own keydown handler
// fire keydown for the shortcut
// assert the textarea handler was not invoked
```