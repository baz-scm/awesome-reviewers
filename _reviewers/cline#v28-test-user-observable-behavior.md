---
title: Test user-observable behavior
description: When code changes affect user input handling (keyboard/mouse/focus) or
  interactive semantics (what element users can activate and how), add or update targeted
  tests that assert the exact user-observable outcome.
repository: cline/cline#v28
label: Testing
language: TSX
comments_count: 2
repository_stars: 70893
---

When code changes affect user input handling (keyboard/mouse/focus) or interactive semantics (what element users can activate and how), add or update targeted tests that assert the exact user-observable outcome.

Practical guidance:
- Keyboard/event suppression: if a keybinding is intended to prevent other components from receiving an event, add a test that the event never reaches the focused component (e.g., textarea input).
- Interactive semantics/accessibility: if the UI is clickable/keyboard-activatable, use semantic elements (e.g., a real `<button type="button">`) and update tests to assert the element type/role so keyboard activation is covered.

Example (testing-library style):
```ts
it("quit shortcut does not reach textarea handlers", async () => {
  const textarea = screen.getByRole("textbox");
  const handler = vi.fn();
  textarea.addEventListener("keydown", handler);

  textarea.focus();
  fireEvent.keyDown(textarea, { key: "q", metaKey: true });

  expect(handler).not.toHaveBeenCalled();
});

it("images notice action is a real button", () => {
  const btn = screen.getByRole("button", { name: /choose model/i });
  expect(btn.tagName).toBe("BUTTON");
});
```

This keeps tests aligned with what users actually experience and prevents regressions in the hardest-to-detect edge cases.