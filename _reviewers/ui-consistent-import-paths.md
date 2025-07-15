---
title: Consistent import paths
description: Establish and follow consistent import path conventions throughout the
  codebase. Prefer aliased imports using the project's path aliases (e.g., `@/src/utils/get-initial-values`)
  over relative imports to ensure consistency and improve maintainability. This practice
  creates uniform import statements across files regardless of their location in the
  project...
repository: shadcn-ui/ui
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 90568
---

Establish and follow consistent import path conventions throughout the codebase. Prefer aliased imports using the project's path aliases (e.g., `@/src/utils/get-initial-values`) over relative imports to ensure consistency and improve maintainability. This practice creates uniform import statements across files regardless of their location in the project structure.

```ts
// Preferred
import { getInitialValues } from "@/src/utils/get-initial-values"

// Instead of
import { getInitialValues } from "../utils/get-initial-values"
```

Using aliased imports makes code more portable and easier to refactor, as moving files doesn't require updating multiple relative import paths. This approach also avoids the confusion that can arise from nested relative paths (e.g., `../../utils/` vs `../utils/`).