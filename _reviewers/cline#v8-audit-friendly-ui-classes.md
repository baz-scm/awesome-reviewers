---
title: Audit-Friendly UI Classes
description: When reviewing UI components, require (a) predictable flex sizing + truncation
  patterns for clickable controls and (b) standardized asset/component usage so presentation
  is easy to audit.
repository: cline/cline#v8
label: Code Style
language: TSX
comments_count: 2
repository_stars: 70867
---

When reviewing UI components, require (a) predictable flex sizing + truncation patterns for clickable controls and (b) standardized asset/component usage so presentation is easy to audit.

**1) Use the correct truncation pattern in flex/tab bars**
- In flex layouts, ensure shrink/truncation works by using `min-w-0` on the flex child/wrapper and `truncate` on the label.
- Avoid scroll/overflow wrappers that clip “attached” visual effects; prefer truncation so the join and adjacent buttons remain visible/clickable.

Example pattern:
```tsx
<div className="flex min-w-0 items-end gap-0.5">
  <span className="min-w-0 truncate">{label}</span>
</div>
```

**2) Standardize icon usage/imports**
- Prefer the project’s canonical icon imports/components (e.g., using the shared `lucide` usage pattern) over custom SVG blocks when the codebase already standardizes the icon.
- This keeps icon usage verifiable and consistent across the UI.

Example intent:
```tsx
import { X } from "lucide-react"; // or the ui package’s canonical icon import

<X className="h-4 w-4" />
```