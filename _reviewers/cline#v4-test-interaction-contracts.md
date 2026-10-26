---
title: Test Interaction Contracts
description: When code changes user interactions (keyboard/global shortcuts, input
  recording, or clickable UI controls), add or update tests to verify the *interaction
  contract*—not just that rendering occurred.
repository: cline/cline#v4
label: Testing
language: TSX
comments_count: 2
repository_stars: 70864
---

When code changes user interactions (keyboard/global shortcuts, input recording, or clickable UI controls), add or update tests to verify the *interaction contract*—not just that rendering occurred.

Apply this as a checklist:
1) For keyboard/event flows, explicitly guard conflicting handlers (e.g., suspend/resume global shortcuts during recording) and test both the “suppressed” period and the “re-enabled after release” behavior.
2) For UI actions, use native interactive elements (e.g., `<button type="button">`) so keyboard activation works by default, and make tests assert the semantic element (real button) rather than only checking classes or role-like behavior.

Example (interaction-suspension test intent):
- Implement suspension during recording
  - call `suspendShortcuts()` when recording starts
  - ensure every relevant handler checks `areShortcutsSuspended()` before acting
- In `keybindings.test.ts`, add a targeted test that verifies shortcuts remain suppressed until all suspensions are released.

Example (accessible control + test intent):
- Render a native button for an action:
```tsx
<button
  type="button"
  data-testid="images-unsupported-choose-model"
  onClick={handleModelButtonClick}
>
  Choose a different model
</button>
```
- In the test, assert the element is a real button (so Enter/Space activation is inherently supported).