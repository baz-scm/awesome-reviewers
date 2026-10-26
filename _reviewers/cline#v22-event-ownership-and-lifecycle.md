---
title: Event Ownership and Lifecycle
description: 'When building interactive React components, make input handling and
  visibility transitions explicit and deterministic: (1) gate handlers/effects with
  clear “ownership” state (e.g., shortcuts suspended, pinned/unpinned, user vs programmatic),
  (2) prevent competing listeners from acting when a component should exclusively
  own the input, (3) design...'
repository: cline/cline#v22
label: React
language: TSX
comments_count: 6
repository_stars: 70886
---

When building interactive React components, make input handling and visibility transitions explicit and deterministic: (1) gate handlers/effects with clear “ownership” state (e.g., shortcuts suspended, pinned/unpinned, user vs programmatic), (2) prevent competing listeners from acting when a component should exclusively own the input, (3) design async/visibility transitions to avoid focus traps or stale UI, and (4) provide keyboard/a11y parity for pointer-driven controls.

Apply this by following patterns like:

- Gate global/UI shortcuts during exclusive interactions:
```ts
useEffect(() => {
  if (!recording) return;
  const onKeyDown = (event: KeyboardEvent) => {
    event.preventDefault();
    event.stopImmediatePropagation(); // don’t let other listeners react
    // ...record the shortcut
  };
  window.addEventListener('keydown', onKeyDown, true);
  return () => window.removeEventListener('keydown', onKeyDown, true);
}, [recording]);
```
…and in every handler that could conflict:
```ts
const onKeyDown = (e: KeyboardEvent) => {
  if (areShortcutsSuspended()) return;
  if (!matchesAccelerator(e, accelerator)) return;
  e.preventDefault();
  e.stopImmediatePropagation();
  // ...handle
};
```

- Distinguish user intent vs programmatic effects for stateful UI (scrolling, resizing, etc.): use refs/targets to avoid treating your own programmatic updates as user actions, and only un-pin/alter state based on the correct input signals.

- Handle hide-vs-unmount carefully: if you “hide” instead of unmounting (e.g., with an Activity/inert pattern), ensure any in-progress async/UI operation is cancelled or state is reset when the component becomes hidden—so the UI returns to a correct, enabled state when shown again.

- Ensure accessibility/keyboard parity for interactive UI elements (e.g., pointer resize handles): add proper roles, focusability, ARIA attributes, and keyboard behaviors with the same affordances (including step/precision rules).
