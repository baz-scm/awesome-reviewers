---
title: Test real interaction boundaries
description: When behavior depends on user interaction (especially keyboard focus/activation),
  write tests that prove the correct boundary is enforced—not just that a handler
  exists.
repository: cline/cline#v16
label: Testing
language: TSX
comments_count: 2
repository_stars: 70882
---

When behavior depends on user interaction (especially keyboard focus/activation), write tests that prove the correct boundary is enforced—not just that a handler exists.

**Apply this by: **
- For keyboard handling, test in the realistic focus context (e.g., textarea/input) and assert the event does not reach other handlers. If you add propagation control, confirm it via an interaction test.
- For clickable UI controls, prefer native interactive elements (e.g., `button type="button"`) and assert the element type in tests so Enter/Space activation works without extra custom wiring.

**Example patterns:**
```ts
// Keyboard/event boundary test idea
it('quit keydown on textarea does not reach textarea handler', () => {
  const handler = vi.fn();
  textarea.addEventListener('keydown', handler);

  // focus textarea, dispatch matching quit keydown
  textarea.focus();
  dispatchKeyDown(textarea, { key: 'q', metaKey: true });

  expect(handler).not.toHaveBeenCalled();
});

// Semantic control test idea
it('uses a real button for link-styled notice', () => {
  const el = screen.getByTestId('images-unsupported-choose-model');
  expect(el.tagName).toBe('BUTTON');
  // optionally: expect(el).toHaveAttribute('type','button')
});
```