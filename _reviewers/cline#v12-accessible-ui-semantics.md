---
title: Accessible UI Semantics
description: "When adding or modifying interactive UI, follow a semantic-and-accessibility-first\
  \ code style:\n\n- Use the correct native element for the interaction.\n  - Don’t\
  \ use <a> for actions. Prefer <button type=\"button\"> for click actions so Enter/Space\
  \ works automatically."
repository: cline/cline#v12
label: Code Style
language: TSX
comments_count: 4
repository_stars: 70872
---

When adding or modifying interactive UI, follow a semantic-and-accessibility-first code style:

- Use the correct native element for the interaction.
  - Don’t use <a> for actions. Prefer <button type="button"> for click actions so Enter/Space works automatically.
- For custom controls, implement required ARIA + keyboard behavior.
  - Example: resize handle should be a focusable control with role="separator" and appropriate aria-valuenow/aria-valuemin/max (as applicable), and respond to Arrow keys (Shift for larger steps).
- Preserve interaction/visual affordances with layout choices.
  - Prefer shrink+truncate over scrolling when overflow would clip an important “attached” visual effect or hide key controls.
- Keep UI component/icon usage consistent for auditability.
  - Prefer a uniform icon import/usage pattern across the codebase so it’s easy to verify what icons are actually used.

Example (native button for an action):
```tsx
{imagesUnsupported && (
  <div role="status" aria-live="polite">
    <button
      type="button"
      onClick={handleModelButtonClick}
      className="underline cursor-pointer"
    >
      Choose another model
    </button>
  </div>
)}
```

Example (accessible custom resize handle skeleton):
```tsx
<div
  role="separator"
  tabIndex={0}
  aria-valuemin={0}
  aria-valuenow={value}
  onKeyDown={(e) => {
    if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
      // apply step; if (e.shiftKey) use larger step
    }
  }}
/>
```