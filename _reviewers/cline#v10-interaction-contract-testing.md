---
title: Interaction Contract Testing
description: 'Add/adjust tests to verify the behavioral contract at integration points—especially
  for keyboard handling and UI semantics.


  - Keyboard/event propagation: when intercepting keys (or preventing default), add
  regression tests that target common receiving elements (e.g., `textarea`, inputs)
  and assert the other handler never runs.'
repository: cline/cline#v10
label: Testing
language: TSX
comments_count: 2
repository_stars: 70869
---

Add/adjust tests to verify the behavioral contract at integration points—especially for keyboard handling and UI semantics.

- Keyboard/event propagation: when intercepting keys (or preventing default), add regression tests that target common receiving elements (e.g., `textarea`, inputs) and assert the other handler never runs.
- DOM semantics/accessibility: when changing element types (e.g., replacing an anchor with a real button), update tests to assert the actual HTML element/type so Enter/Space activation works as expected.

Example (event non-leak regression):
```ts
it("quit keydown does not reach textarea handler", () => {
  const textarea = screen.getByRole("textbox");
  const onKeyDown = jest.fn();
  textarea.addEventListener("keydown", onKeyDown);

  fireEvent.keyDown(textarea, { key: "q", metaKey: true });

  expect(onKeyDown).not.toHaveBeenCalled();
});
```

Example (semantic element assertion):
```ts
it("renders a real button for the image-notice action", () => {
  const button = screen.getByRole("button", {
    name: /choose model/i,
  });
  expect(button).toBeInstanceOf(HTMLButtonElement);
});
```