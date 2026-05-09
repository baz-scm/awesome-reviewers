---
title: Organize and Clean Imports
description: 'Keep codebase structure and import usage aligned with the intended architecture
  and boundaries.


  - **Place files in the correct feature/module directory** (e.g., shared UI utilities
  under `src/features/shared/`), rather than leaving them in a generic `utils/` folder
  when the architecture expects otherwise.'
repository: coleam00/Archon
label: Code Style
language: TypeScript
comments_count: 3
repository_stars: 21089
---

Keep codebase structure and import usage aligned with the intended architecture and boundaries.

- **Place files in the correct feature/module directory** (e.g., shared UI utilities under `src/features/shared/`), rather than leaving them in a generic `utils/` folder when the architecture expects otherwise.
- **Respect intended coupling boundaries**: if a workflow/tooling script is designed to be standalone (e.g., a Bun CLI wrapper), avoid importing monorepo packages that would force bundling or introduce runtime dependency coupling.
- **Enforce import hygiene**: remove unused imports; for TypeScript/React types used only at compile time, use `import type`.

Example:
```ts
// ✅ type-only import to avoid unused/runtime imports
import type React from 'react';

// ✅ do not import values you never use
// import { useToast } from '../contexts/ToastContext'; // remove if unused
```