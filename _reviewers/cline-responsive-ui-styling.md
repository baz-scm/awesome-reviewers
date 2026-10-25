---
title: Responsive UI Styling
description: When styling interactive UI (tabs, drawers, dialogs), ensure layout decisions
  remain usable under constrained sizes and keep implementation consistent with shared
  UI primitives.
repository: CLINE/CLINE
label: Code Style
language: TSX
comments_count: 3
repository_stars: 70837
---

When styling interactive UI (tabs, drawers, dialogs), ensure layout decisions remain usable under constrained sizes and keep implementation consistent with shared UI primitives.

- For tab/strip labels and similar control rows:
  - Prefer flex-shrink + truncation instead of scrolling/clipping that can hide or detach controls.
  - Apply `min-w-0` to wrappers and `truncate` (ellipsis) to the label region, so controls like “+”/hide remain clickable.
  - Avoid layouts that clip “attached” visuals (e.g., switching from a scrolling strip to shrink/truncate if clipping breaks the look).

  Example pattern:
  ```tsx
  <div className="flex h-9 items-end gap-1">
    <div className="flex min-w-0 items-end gap-0.5">
      <div className="min-w-0 truncate">Very long label…</div>
    </div>
    <button type="button">+</button>
    <button type="button">Hide</button>
  </div>
  ```

- For dialogs/drawers in small viewports:
  - Cap by viewport height (e.g., `max-h-[calc(100dvh-2rem)]`) and enable internal scrolling so key actions remain reachable.

- For shared UI elements (icons/buttons):
  - Use the standardized icon component/import pattern (e.g., `lucide-react` named icons with consistent props) rather than mixing in ad-hoc inline SVGs, so code review can reliably confirm icon consistency.