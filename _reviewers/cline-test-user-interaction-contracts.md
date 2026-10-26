---
title: Test user interaction contracts
description: 'When you change keyboard handling or interactive UI elements, update
  tests to lock in the user-visible interaction contract—not just internal logic.


  Concretely:'
repository: Cline/Cline
label: Testing
language: TSX
comments_count: 2
repository_stars: 70840
---

When you change keyboard handling or interactive UI elements, update tests to lock in the user-visible interaction contract—not just internal logic.

Concretely:
- Keyboard shortcuts: add tests that assert the shortcut keydown reaches the intended handler and does **not** propagate to other focused controls (e.g., textareas).
- Accessibility/semantics: if the element is user-activated via keyboard, use native controls (e.g., `<button type="button">`) and assert in tests that the correct semantic element is rendered.

Example (React Testing Library style):
```ts
import { render, fireEvent } from "@testing-library/react";

test("quit keydown does not reach textarea handler", () => {
  const onTextareaKeyDown = jest.fn();
  const { getByRole } = render(
    <textarea onKeyDown={onTextareaKeyDown} />
  );

  fireEvent.keyDown(window, { key: "q", metaKey: true });

  expect(onTextareaKeyDown).not.toHaveBeenCalled();
});

test("images unsupported notice uses a native button", () => {
  const { getByTestId } = render(/* component */);
  const el = getByTestId("images-unsupported-choose-model");
  expect(el.tagName.toLowerCase()).toBe("button");
});
```

This prevents regressions where keyboard shortcuts or activation behavior subtly breaks inputs or accessibility expectations.