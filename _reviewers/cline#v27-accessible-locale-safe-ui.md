---
title: Accessible, Locale-safe UI
description: 'When implementing UI behaviors and user-facing text, follow a consistent
  standard:


  1) Make interactive controls semantic and keyboard-accessible

  - Use the correct ARIA role(s) for non-standard controls (e.g., resize handles),
  set relevant aria attributes (like min/max/current values), and ensure the element
  is focusable.'
repository: cline/cline#v27
label: Code Style
language: TSX
comments_count: 3
repository_stars: 70892
---

When implementing UI behaviors and user-facing text, follow a consistent standard:

1) Make interactive controls semantic and keyboard-accessible
- Use the correct ARIA role(s) for non-standard controls (e.g., resize handles), set relevant aria attributes (like min/max/current values), and ensure the element is focusable.
- Provide keyboard interaction that matches the pointer behavior (e.g., ArrowUp/ArrowDown resize; Shift for step changes).

2) Compose translated summaries with locale-correct formatting
- Don’t hardcode punctuation or assume word order.
- Build each “part” as a self-contained verb phrase in translation (e.g., “files read”, “folders listed”), and join them using locale-aware formatting (e.g., `Intl.ListFormat`) instead of fixed `", "`.
- Provide a clear fallback when there is no content to summarize.

3) Keep dialogs/actions reachable in small viewports
- Cap dialog height to the available viewport height (`max-h-[calc(100dvh-…)]`) and enable internal scrolling so secondary actions remain reachable.

Example patterns (TypeScript/React):

// 1) Resize handle semantics + keyboard support
<div
  role="separator"
  tabIndex={0}
  aria-valuemin={min}
  aria-valuemax={max}
  aria-valuenow={value}
  onKeyDown={(e) => {
    const step = e.shiftKey ? largeStep : smallStep;
    if (e.key === 'ArrowDown') onHeightChange(value - step);
    if (e.key === 'ArrowUp') onHeightChange(value + step);
  }}
  onPointerDown={/* pointer resize logic */}
/>

// 2) Locale-safe join for translated list items
const items = [
  t('...files', { count: nFiles }),
  t('...folders', { count: nFolders }),
].filter(Boolean);

if (items.length === 0) return t('...fallback');

const list = new Intl.ListFormat(locale, { style: 'long', type: 'conjunction' }).format(items);
return t('...summaryPrefix', { items: list });

// 3) Viewport-safe dialog container
<DialogContent className="max-h-[calc(100dvh-2rem)] overflow-y-auto" />