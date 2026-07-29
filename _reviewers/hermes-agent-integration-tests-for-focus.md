---
title: Integration tests for focus
description: When behavior depends on library primitives (e.g., Radix) and real browser
  focus/pointer flows (including `document.body` portals), unit tests that reimplement
  internal handlers are not enough. Write tests that render the actual component tree
  and assert user-observable outcomes.
repository: nousresearch/hermes-agent
label: Testing
language: TSX
comments_count: 2
repository_stars: 221948
---

When behavior depends on library primitives (e.g., Radix) and real browser focus/pointer flows (including `document.body` portals), unit tests that reimplement internal handlers are not enough. Write tests that render the actual component tree and assert user-observable outcomes.

Apply this standard:
- Render the real primitive/component (not a re-copied `onOpenChange`/handler) and assert the final DOM state (e.g., tooltip open/closed) and/or event delivery.
- Cover both mouse/pointer focus paths and keyboard/a11y paths (e.g., `:focus-visible`) and keep the expectations aligned to how the product behaves.
- For portal-based content, include a regression test that matches the real DOM topology (focus moving into portal content should not trigger the incorrect “retract” behavior).

Example pattern (tooltip cancellation):
```ts
// Pseudocode: render actual TooltipPrimitive-based component
render(
  <TooltipRoot /* real component */>
    <TooltipTrigger asChild>
      <button>Tip</button>
    </TooltipTrigger>
    <TooltipContent>...</TooltipContent>
  </TooltipRoot>
)

// Mouse/focus path should NOT open
userEvent.click(screen.getByRole('button', { name: /tip/i }))
expect(screen.queryByText('...')).not.toBeInTheDocument()

// Keyboard focus path SHOULD open
screen.getByRole('button', { name: /tip/i }).focus()
expect(screen.getByText('...')).toBeInTheDocument()
```
This ensures the test verifies the real cancellation mechanism and prevents regressions involving focus and portal DOM behavior.