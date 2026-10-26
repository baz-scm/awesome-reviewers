---
title: Test Interaction Contracts
description: When changing user interaction behavior, add/adjust tests that verify
  the externally observable interaction contract in realistic DOM contexts—especially
  keyboard handling and interactive control semantics.
repository: cline/cline#v15
label: Testing
language: TSX
comments_count: 2
repository_stars: 70877
---

When changing user interaction behavior, add/adjust tests that verify the externally observable interaction contract in realistic DOM contexts—especially keyboard handling and interactive control semantics.

Apply this by:
- Keyboard/event consumption: simulate keydown on elements that commonly intercept input (e.g., a focused `<textarea>`), and assert the expected handler runs while competing handlers never receive the event.
- Accessibility/activation semantics: use native controls (`<button type="button">` for actions). Tests should assert the element’s real semantic type, and (optionally) that Enter/Space activation triggers the handler.

Example (keyboard propagation test idea):
```ts
// Arrange: focus a textarea, attach both the global shortcut and the textarea handler
textarea.focus();
const textareaHandler = vi.fn();
textarea.addEventListener('keydown', textareaHandler);

// Act: dispatch the quit shortcut keydown
window.dispatchEvent(new KeyboardEvent('keydown', { key: 'q', metaKey: true }));

// Assert: textarea never sees the key
expect(textareaHandler).not.toHaveBeenCalled();
```