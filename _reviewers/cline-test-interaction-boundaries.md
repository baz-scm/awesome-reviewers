---
title: Test Interaction Boundaries
description: 'When code changes affect keyboard/focus behavior or interactive UI semantics,
  add regression tests that prove the intended interaction boundary.


  Apply this by:'
repository: CLINE/cline
label: Testing
language: TSX
comments_count: 2
repository_stars: 70839
---

When code changes affect keyboard/focus behavior or interactive UI semantics, add regression tests that prove the intended interaction boundary.

Apply this by:
- Keyboard/shortcut handlers: add tests that assert the matched keydown/up does *not* reach underlying focused components (e.g., textarea/chat input). Ensure the test simulates the relevant focus target.
- UI controls: use semantic HTML for actions (e.g., `<button type="button">` instead of an anchor with click handlers) and add tests that assert the correct element type/role so keyboard activation is preserved.

Example test intents (pattern):
```ts
// 1) Shortcut does not leak to textarea handler
it('does not reach textarea handler', () => {
  render(<ChatTextArea />);
  const textarea = screen.getByRole('textbox');
  textarea.focus();
  fireEvent.keyDown(textarea, { key: 'q', metaKey: true });
  expect(onTextareaKeydown).not.toHaveBeenCalled();
});

// 2) Interactive element uses real button semantics
it('renders a real button for activation', () => {
  render(<ImagesUnsupportedNotice />);
  expect(screen.getByRole('button', { name: /choose model/i })).toBeInTheDocument();
});
```