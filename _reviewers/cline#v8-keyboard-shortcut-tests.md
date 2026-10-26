---
title: Keyboard shortcut tests
description: For keyboard/shortcut features with global listeners and cross-component
  side effects, add tests that verify both (1) lifecycle/state gating and (2) event
  propagation blocking.
repository: cline/cline#v8
label: Testing
language: TSX
comments_count: 2
repository_stars: 70867
---

For keyboard/shortcut features with global listeners and cross-component side effects, add tests that verify both (1) lifecycle/state gating and (2) event propagation blocking.

Apply this standard by:
- Suspension/state coverage: if the UI temporarily disables shortcuts (e.g., during recording), unit-test that suspension is applied and that handlers refuse to act until *all* suspensions are released (reference-counting).
- Propagation coverage: when a keydown must not reach other UI (especially inputs like textareas), add a DOM/integration test that confirms the competing handler is never invoked for a matched shortcut keydown.
- Assert the observable outcomes: 
  - shortcut handler does not update/quit while suspended
  - other component handlers (e.g., textarea `onKeyDown`) never fire when the shortcut is matched

Example (test intent modeled after the fixes):
```ts
// 1) Suspension lifecycle: handlers must respect areShortcutsSuspended()
it("suspends shortcuts until every suspension is released", () => {
  suspendShortcuts();
  suspendShortcuts();
  // emit keydown that would normally trigger quit/shortcuts
  // expect: handler not invoked
  releaseSuspension();
  // expect: still not invoked
  releaseSuspension();
  // expect: now invoked
});

// 2) Propagation blocking: textarea must not receive quit shortcut
it("quit keydown on textarea never reaches its handler", () => {
  const textarea = document.createElement("textarea");
  const onKeyDown = vi.fn();
  textarea.addEventListener("keydown", onKeyDown);
  document.body.appendChild(textarea);
  textarea.focus();

  dispatchKeydown({ key: "q", metaKey: true /* mac example */ });
  expect(onKeyDown).not.toHaveBeenCalled();
});
```
This keeps shortcut behavior deterministic and prevents regressions where shortcuts accidentally trigger while recording or leak into form controls.