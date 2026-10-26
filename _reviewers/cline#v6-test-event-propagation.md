---
title: Test event propagation
description: For keyboard-driven (and other DOM-event-driven) UI flows with guards
  like shortcut suspension, “hold” handlers, or focus-sensitive behaviors, always
  add regression tests that prove (1) the event is captured only when intended, and
  (2) other handlers do not receive the same event.
repository: cline/cline#v6
label: Testing
language: TSX
comments_count: 3
repository_stars: 70864
---

For keyboard-driven (and other DOM-event-driven) UI flows with guards like shortcut suspension, “hold” handlers, or focus-sensitive behaviors, always add regression tests that prove (1) the event is captured only when intended, and (2) other handlers do not receive the same event.

Apply this by testing:
- **Propagation leakage**: when your handler matches, assert the event doesn’t reach the would-be consumer (e.g., textarea/chat input).
- **Focus targeting**: arrow keys / commands should not trigger when a focused child control is the event target.
- **Guard/suspension semantics**: when you suspend behavior, tests must cover both “suspended” and “released” states (including reference-counted/stacked suspensions).

Example pattern (JSDOM/Vitest-style):
```ts
import { describe, it, expect, vi } from 'vitest';

it('does not reach textarea handler on quit keydown', () => {
  const textarea = document.createElement('textarea');
  document.body.appendChild(textarea);
  textarea.focus();

  const onTextareaKeyDown = vi.fn();
  textarea.addEventListener('keydown', onTextareaKeyDown);

  // Dispatch the keydown that the app should intercept.
  const event = new KeyboardEvent('keydown', { key: 'q', metaKey: true, bubbles: true });
  window.dispatchEvent(event);

  // Regression assertion: intercepted events must not be observed by textarea.
  expect(onTextareaKeyDown).not.toHaveBeenCalled();
});
```

Use the same approach to test focus-sensitive child controls (e.g., ensure arrow keys aimed at a focused button/disclosure don’t trigger scroll/pin changes), and suspension guard release (e.g., verify the shortest path “suspended until every release occurs”).