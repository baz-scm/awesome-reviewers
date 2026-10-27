---
title: Config Directives Placement
description: When adding configuration controls (feature-flag pragmas, compiler/test
  directives, or config-driven imports), follow the exact conventions your tooling
  expects.
repository: facebook/react#b16
label: Configurations
language: TSX
comments_count: 2
repository_stars: 251891
---

When adding configuration controls (feature-flag pragmas, compiler/test directives, or config-driven imports), follow the exact conventions your tooling expects.

- **Pragma/comment directives:** Ensure all `// @...` directives are placed **on the first line(s)** of the file/fixture so the compiler/test harness can reliably detect them. Otherwise, you may unintentionally pick up **default behavior** and see confusing errors.
- **Config-related imports:** Use the **established import paths** that match the current multi-workspace build setup. Don’t switch between source vs `dist` entrypoints ad-hoc—standardize via an alias only after it’s an agreed change.

Example (pragma placement):
```ts
// @enableInferEventHandlers
// @validateRefAccessDuringRender
// (no other leading comments/imports before these)

export function test() {}
```

Example (consistent config-driven import path):
```ts
import {ErrorCategory} from 'babel-plugin-react-compiler/dist/CompilerError';
```