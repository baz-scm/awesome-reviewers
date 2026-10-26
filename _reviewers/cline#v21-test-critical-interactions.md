---
title: Test critical interactions
description: 'When behavior depends on user interaction details (keyboard events,
  focus, accessibility semantics), encode those guarantees in tests.


  - Keyboard/shortcut handlers: add tests that simulate the relevant keydown on the
  actual focused element and assert the intended handler fires *only* where expected
  (and does not leak to other components).'
repository: cline/cline#v21
label: Testing
language: TSX
comments_count: 2
repository_stars: 70886
---

When behavior depends on user interaction details (keyboard events, focus, accessibility semantics), encode those guarantees in tests.

- Keyboard/shortcut handlers: add tests that simulate the relevant keydown on the actual focused element and assert the intended handler fires *only* where expected (and does not leak to other components).
- Accessibility/semantics: prefer native controls (e.g., `<button type="button">`) and write tests that assert the correct element role/type, not just styling.

Example (keyboard propagation + semantics):
```ts
// keyboard/shortcut: ensure it doesn't reach textarea handler
fireEvent.keyDown(textarea, { key: 'q', metaKey: true });
expect(chatInputOnKeyDown).not.toHaveBeenCalled();

// semantics: ensure native button
const el = screen.getByTestId('images-unsupported-choose-model');
expect(el.tagName).toBe('BUTTON');
fireEvent.keyDown(el, { key: 'Enter' });
expect(handleModelButtonClick).toHaveBeenCalled();
```