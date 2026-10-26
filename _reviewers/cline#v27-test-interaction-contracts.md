---
title: Test Interaction Contracts
description: Add/update tests to verify the full interaction contract of UI behavior—not
  just the “happy path.” For event-driven UI, assert that keyboard/mouse events reach
  only the intended handler (and don’t leak to inputs). For interactive controls,
  assert semantic correctness (use real elements like `<button>` rather than clickable
  anchors) so keyboard activation...
repository: cline/cline#v27
label: Testing
language: TSX
comments_count: 2
repository_stars: 70892
---

Add/update tests to verify the full interaction contract of UI behavior—not just the “happy path.” For event-driven UI, assert that keyboard/mouse events reach only the intended handler (and don’t leak to inputs). For interactive controls, assert semantic correctness (use real elements like `<button>` rather than clickable anchors) so keyboard activation (Enter/Space) works and tests enforce the semantic element type.

Example (keyboard event boundary):
```ts
// pseudo-test
it('does not let quit keydown reach textarea handlers', () => {
  const textarea = screen.getByRole('textbox');
  textarea.focus();

  const handler = vi.fn();
  // attach handler as your page-level shortcut/input handler would
  textarea.addEventListener('keydown', handler);

  fireEvent.keyDown(textarea, { key: 'q', metaKey: true });

  expect(handler).not.toHaveBeenCalled();
});
```

Example (semantic interactive element):
```ts
it('renders a real button for the link-like action', () => {
  render(<YourComponent />);
  const el = screen.getByTestId('images-unsupported-choose-model');
  expect(el.tagName).toBe('BUTTON');
  expect(el).toHaveAttribute('type', 'button');
});
```