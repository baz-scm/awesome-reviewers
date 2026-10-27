---
title: Configuration Directive Placement
description: 'Ensure configuration and feature-flag directives are applied in the
  exact way the tooling expects, and keep configuration-related wiring consistent.


  Apply:'
repository: facebook/react#b7
label: Configurations
language: TSX
comments_count: 2
repository_stars: 251888
---

Ensure configuration and feature-flag directives are applied in the exact way the tooling expects, and keep configuration-related wiring consistent.

Apply:
- Put any tool-specific `@` pragmas (feature flags/validation toggles) at the very top of the file (first lines). Don’t rely on them being detected later in the file.
- Assume validations/behaviors may be enabled by default; if you’re seeing unexpected errors, verify the intended pragma placement and that the correct flag is being activated.
- For configuration-related exports (e.g., error categories), follow the established import path/style across the repo; introduce aliasing only after a deliberate multi-workspace plan.

Example (pragma placement):
```ts
// @enableInferEventHandlers
// @validateRefAccessDuringRender

// ...rest of the file (components/test fixtures/etc.)
```

If you need to change import paths for configuration-related types, do it via a planned alias rather than one-off adjustments, to keep behavior consistent across workspaces.