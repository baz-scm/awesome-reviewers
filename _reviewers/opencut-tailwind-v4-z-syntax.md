---
title: Tailwind v4 Z Syntax
description: When using Tailwind CSS v4, follow the v4-supported utility syntax for
  z-index and similar numeric utilities. Prefer the non-bracket form `z-<number>`
  (e.g., `z-150`, `z-200`) instead of `z-[<number>]`; the JIT compiler will handle
  arbitrary numeric values and won’t drop these classes.
repository: opencut-app/opencut
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 81817
---

When using Tailwind CSS v4, follow the v4-supported utility syntax for z-index and similar numeric utilities. Prefer the non-bracket form `z-<number>` (e.g., `z-150`, `z-200`) instead of `z-[<number>]`; the JIT compiler will handle arbitrary numeric values and won’t drop these classes.

Example:
```tsx
<div className="absolute pointer-events-auto z-150" />
<ContextMenuContent className="z-200" />
```