---
title: Configuration-sensitive directives
description: When code relies on tooling configuration (compiler pragmas/feature flags
  or workspace-specific module resolution), follow the tool’s exact expectations.
  Misplaced directives or “convenient” import paths can cause failures that look unrelated.
repository: facebook/react#b2
label: Configurations
language: TSX
comments_count: 2
repository_stars: 251882
---

When code relies on tooling configuration (compiler pragmas/feature flags or workspace-specific module resolution), follow the tool’s exact expectations. Misplaced directives or “convenient” import paths can cause failures that look unrelated.

- Pragmas/feature-flag directives:
  - If the file header includes @ directives (e.g., compiler/plugin pragmas), place them on the very first line(s) of the file in the required order/format.
  - Assume related validations may be enabled by default; incorrect placement can trigger errors.

- Build/config-dependent imports:
  - Import from the module entrypoint path that matches the current build setup (commonly the built output, e.g., dist/*, rather than src/*).
  - Keep the import style consistent across the repo; only introduce aliases/path simplifications when your multi-workspace build supports them.

Example (pragma placement):
```ts
// @enableInferEventHandlers
// @validateRefAccessDuringRender

export function MyComponent() {
  // ...
}
```

Example (config-aligned import path):
```ts
import {ErrorCategory} from 'babel-plugin-react-compiler/dist/CompilerError';
```