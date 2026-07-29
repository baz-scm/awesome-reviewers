---
title: Action slot invariants
description: 'When building React “action slot” containers (inline vs overflow menus,
  responsive headers, hold/click controls), enforce these invariants:


  1) **Preserve host mount semantics**'
repository: QwenLM/qwen-code
label: React
language: TSX
comments_count: 6
repository_stars: 26407
---

When building React “action slot” containers (inline vs overflow menus, responsive headers, hold/click controls), enforce these invariants:

1) **Preserve host mount semantics**
- Don’t render the same `children` in multiple parallel trees just to measure layout.
- Avoid unmounting/remounting stateful host actions during responsive collapse/expand if the host’s state/subscriptions must persist.

2) **Preserve DOM identity for event guarantees**
- For interactions relying on pointer capture, focus, or other event invariants, keep the captured element mounted (or handle release/cancel at a higher level like `document`).

3) **Normalize host output before applying `asChild`/DOM-level props**
- If the host can return `<>...</>` Fragments (or nested Fragments), flatten/normalize to concrete elements before wrapping with `<DropdownMenuItem asChild>` (or before cloning/annotating).

4) **Use the menu framework’s item components for accessibility + behavior**
- Don’t place raw action buttons directly under `DropdownMenuContent`. Wrap each action with the framework’s item component (e.g., `DropdownMenuItem asChild`) so roles/keyboard navigation and menu auto-close work consistently.

5) **Don’t rely on custom components forwarding unknown props**
- Avoid `cloneElement` to inject `data-*` or handlers unless you can guarantee the host component forwards unknown props via `...rest`.
- Prefer wrapping with a simple DOM element (e.g., `<span style={{display:'contents'}} data-...>...</span>`) so your attributes always land in the DOM.

Example pattern (flatten + menu items + safe wrappers, no Fragment targets):
```tsx
import { Children, Fragment, isValidElement, useMemo } from 'react';

function flattenToElements(node: React.ReactNode) {
  const out: React.ReactElement[] = [];
  for (const child of Children.toArray(node)) {
    if (!isValidElement(child)) continue;
    if (child.type === Fragment) {
      out.push(...flattenToElements((child.props as any).children));
    } else {
      out.push(child);
    }
  }
  return out;
}

function OverflowMenu({ children }: { children: React.ReactNode }) {
  const elements = useMemo(() => flattenToElements(children), [children]);

  return (
    <DropdownMenuContent>
      {elements.map((el, i) => (
        <DropdownMenuItem key={el.key ?? i} asChild>
          <span style={{ display: 'contents' }} data-action-index={String(i)}>
            {el}
          </span>
        </DropdownMenuItem>
      ))}
    </DropdownMenuContent>
  );
}
```

Applying these rules prevents: duplicated subscriptions (double mount), broken menu roles/keyboard behavior (raw children), invalid DOM prop application to Fragments, click-proxy failures from missing prop forwarding, and interaction bugs from DOM identity changes during state transitions.