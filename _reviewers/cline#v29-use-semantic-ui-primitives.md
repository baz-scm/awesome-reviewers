---
title: Use Semantic UI Primitives
description: 'For UI code, follow two consistent patterns:


  1) Prefer native interactive elements for actions

  - Use `<button type="button">` for clickable actions (not anchors with click handlers).'
repository: cline/cline#v29
label: Code Style
language: TSX
comments_count: 2
repository_stars: 70893
---

For UI code, follow two consistent patterns:

1) Prefer native interactive elements for actions
- Use `<button type="button">` for clickable actions (not anchors with click handlers).
- Ensure keyboard activation works by default (Enter/Space) and keep tests asserting the semantic element.

2) Keep common UI assets consistent
- For standard icons (e.g., Lucide icons available in your UI packages), use the shared icon component/import pattern rather than custom/inline SVG variants, so it’s easy to confirm the exact icon used and avoid visual/behavior drift.

Example (semantic action):
```tsx
<button
  type="button"
  onClick={handleModelButtonClick}
  className="underline cursor-pointer"
  data-testid="images-unsupported-choose-model"
>
  Choose a supported model
</button>
```

Example (standard icon usage):
```tsx
import { X } from "lucide"; // or the package’s shared UI import

<X className="h-4 w-4" />
```