---
title: Consistent directives and imports
description: 'When code depends on tooling directives or shared conventions, follow
  placement and organization rules exactly.


  - Tooling pragmas / directives: Ensure all leading `@` pragmas required by the build/test
  tooling are placed at the very top of the file (typically the first lines), with
  no preceding comments or whitespace. Misplacement can change defaults...'
repository: facebook/react#b1
label: Code Style
language: TSX
comments_count: 2
repository_stars: 251878
---

When code depends on tooling directives or shared conventions, follow placement and organization rules exactly.

- Tooling pragmas / directives: Ensure all leading `@` pragmas required by the build/test tooling are placed at the very top of the file (typically the first lines), with no preceding comments or whitespace. Misplacement can change defaults (e.g., validation toggles) and cause failures.

- Imports: Keep import style and module path patterns consistent across the codebase. If you need to change import sources (e.g., from one path to another) or introduce aliases, do so intentionally and consistently—defer broader alias refactors to a dedicated follow-up.

Example (directives at top):
```ts
// @enableInferEventHandlers
// @validateRefAccessDuringRender

// rest of the file...
```

Example (consistent import style):
```ts
import {ErrorCategory} from 'babel-plugin-react-compiler/dist/CompilerError';
```