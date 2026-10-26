---
title: Accessible Responsive UI
description: 'When building UI components (especially overlays/dialogs and inline
  actions), follow a consistent markup/style standard:


  1) Make overlays responsive

  - Cap height to the viewport and allow scrolling so key actions remain reachable
  in short windows.'
repository: cline/cline#v6
label: Code Style
language: TSX
comments_count: 2
repository_stars: 70864
---

When building UI components (especially overlays/dialogs and inline actions), follow a consistent markup/style standard:

1) Make overlays responsive
- Cap height to the viewport and allow scrolling so key actions remain reachable in short windows.
- Prefer patterns like: `max-h-[calc(100dvh-2rem)]` + scrolling.

2) Use native interactive semantics
- Don’t attach click handlers to anchors unless you’re actually navigating.
- For actions that trigger behavior (e.g., choosing a model), use `<button type="button">` so Enter/Space work automatically.
- Update tests to assert the semantic element (button vs anchor).

Example (combined):
```tsx
// Overlay: responsive sizing
<Dialog open={open} onOpenChange={onOpenChange}>
  <DialogContent
    className="max-h-[calc(100dvh-2rem)] overflow-auto outline-none"
  >
    {/* content */}
    <button type="button" onClick={handleOpenConnectors}>
      Open Connectors
    </button>
  </DialogContent>
</Dialog>

// Action: native button (not anchor)
{imagesUnsupported && (
  <button
    type="button"
    className="underline cursor-pointer"
    onClick={handleModelButtonClick}
  >
    Choose a different model
  </button>
)}
```

Adopting this reduces UI breakage in small viewports and prevents accessibility regressions from non-semantic interactive elements.