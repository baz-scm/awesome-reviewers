---
title: Convention-First Code Style
description: 'When code relies on special syntax or build conventions, follow the
  prescribed placement and import patterns exactly—don’t assume defaults.


  - File-level pragmas/directives: ensure all `// @...` pragmas are placed at the
  very top of the file (starting on the first line(s) as required). Misplacement can
  change behavior because some features may be enabled by...'
repository: facebook/react#b4
label: Code Style
language: TSX
comments_count: 2
repository_stars: 251885
---

When code relies on special syntax or build conventions, follow the prescribed placement and import patterns exactly—don’t assume defaults.

- File-level pragmas/directives: ensure all `// @...` pragmas are placed at the very top of the file (starting on the first line(s) as required). Misplacement can change behavior because some features may be enabled by default.
- Imports across workspaces: keep a consistent import style using the established module entrypoints/paths. Avoid ad-hoc path changes; if you want aliases to simplify imports, treat it as a separate build/setup improvement.

Example (pragma placement):
```ts
// @enableInferEventHandlers
// @validateRefAccessDuringRender

// ...rest of file
```

Example (consistent import style):
```ts
import {ErrorCategory} from 'babel-plugin-react-compiler/dist/CompilerError';
```