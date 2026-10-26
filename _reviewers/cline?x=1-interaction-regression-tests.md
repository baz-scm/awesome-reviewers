---
title: Interaction regression tests
description: Whenever you change keyboard handling or interactive UI, add targeted
  tests that simulate the real user trigger (focus target + key activation) and assert
  the concrete behavioral/semantic outcome—so regressions don’t slip in.
repository: cline/cline?x=1
label: Testing
language: TSX
comments_count: 2
repository_stars: 70861
---

Whenever you change keyboard handling or interactive UI, add targeted tests that simulate the real user trigger (focus target + key activation) and assert the concrete behavioral/semantic outcome—so regressions don’t slip in.

Checklist
- Keyboard/event changes: test with the real focus context (e.g., textarea/input) and assert the event does *not* reach unintended handlers.
- UI accessibility/activation changes: prefer native controls (e.g., `button`) and test for the actual element type/roles, not just styling or `onClick`.

Example (event propagation regression)
```ts
it('quit keydown on textarea never reaches its handler', () => {
  const textarea = document.createElement('textarea');
  document.body.appendChild(textarea);
  const handler = vi.fn();
  textarea.addEventListener('keydown', handler);

  // focus target
  textarea.focus();

  // simulate quit shortcut keydown
  fireEvent.keyDown(textarea, { key: 'q', metaKey: true });

  expect(handler).not.toHaveBeenCalled();
});
```

Example (semantic control test)
```ts
it('renders a real button for Enter/Space activation', () => {
  render(<ChatTextArea ... />);
  const el = screen.getByTestId('images-unsupported-choose-model');
  expect(el.tagName).toBe('BUTTON');
  expect(el).toHaveAttribute('type', 'button');
});
```