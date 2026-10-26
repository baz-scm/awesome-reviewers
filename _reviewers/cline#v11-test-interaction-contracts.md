---
title: Test interaction contracts
description: 'When code changes affect user input or keyboard interaction, add/adjust
  tests to enforce the interaction contract end-to-end: (1) key events must be handled/prevented
  so they don’t reach unintended listeners, and (2) interactive UI controls must use
  native semantics so keyboard activation works.'
repository: cline/cline#v11
label: Testing
language: TSX
comments_count: 2
repository_stars: 70871
---

When code changes affect user input or keyboard interaction, add/adjust tests to enforce the interaction contract end-to-end: (1) key events must be handled/prevented so they don’t reach unintended listeners, and (2) interactive UI controls must use native semantics so keyboard activation works.

Apply it like this:
- For keyboard/event handling changes: write a regression test that the target keydown is intercepted (and not observed by the “wrong” component), including the relevant DOM context (e.g., a textarea/contenteditable).
- For UI control changes: assert the rendered element’s semantic role (e.g., a real `button`) rather than only styling or click behavior.

Example test patterns (conceptual):
```ts
// 1) Keyboard propagation regression
it('does not let quit keydown reach textarea handler', () => {
  const textarea = screen.getByRole('textbox');
  const handler = vi.fn();
  textarea.addEventListener('keydown', handler);

  fireEvent.keyDown(textarea, { key: 'q', metaKey: true });

  expect(handler).not.toHaveBeenCalled();
});

// 2) Semantic control regression
it('renders a real button for keyboard activation', () => {
  render(<YourComponent />);

  expect(screen.getByRole('button', { name: /choose model/i })).toBeInstanceOf(HTMLButtonElement);
});
```
This keeps tests aligned to what users experience (keyboard + interaction semantics), preventing regressions like event leakage and broken Enter/Space behavior.