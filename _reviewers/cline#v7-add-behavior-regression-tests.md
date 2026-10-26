---
title: Add Behavior Regression Tests
description: When changes affect user-interaction behavior (keyboard shortcuts/event
  propagation or interactive control semantics), add or update focused tests that
  lock in the intended outcome.
repository: cline/cline#v7
label: Testing
language: TSX
comments_count: 2
repository_stars: 70865
---

When changes affect user-interaction behavior (keyboard shortcuts/event propagation or interactive control semantics), add or update focused tests that lock in the intended outcome.

Apply this by:
- Keyboard/event routing: add a regression test that proves the intercepted key event does *not* reach the underlying input/handler (e.g., textarea/chat input).
- Accessibility/interaction semantics: when swapping UI elements for correct keyboard/assistive behavior, ensure tests assert the semantic element/type (e.g., a real `<button type="button">`, not an anchor pretending to be a button).

Example (keyboard event regression test idea):
```ts
// Arrange: render component with textarea/input + quit handler
// Act: dispatch a matching quit keydown while focus is on textarea
// Assert: textarea/input handler was NOT called
expect(textareaHandler).not.toHaveBeenCalled();
```

Example (semantic assertion idea):
```ts
const el = screen.getByTestId('images-unsupported-choose-model');
expect(el.tagName).toBe('BUTTON');
expect(el).toHaveAttribute('type', 'button');
```