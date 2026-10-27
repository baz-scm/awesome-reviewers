---
title: Configuration pragma consistency
description: 'Ensure configuration directives that control compiler/tooling behavior
  are applied deterministically and via the expected entrypoints.


  1) Place feature/pragmas correctly'
repository: facebook/react#b12
label: Configurations
language: TSX
comments_count: 2
repository_stars: 251896
---

Ensure configuration directives that control compiler/tooling behavior are applied deterministically and via the expected entrypoints.

1) Place feature/pragmas correctly
- Any compiler directives (e.g., `// @enable...`, `// @validate...`) must appear on the first line(s) of the file so they are actually parsed/applied.
- If a validation flag is enabled by default, missing/incorrect pragmas can surface unexpected failures—so keep pragma placement consistent across fixtures and test files.

2) Use stable, expected import paths for tooling/config
- For configuration-adjacent exports (errors/categories, compiler entrypoints, etc.), prefer the public/module path your build tooling expects (often `dist/...`) rather than `src/...`.
- If simplification (aliases) is desired, address it later—don’t mix styles in the same codebase.

Example:
```ts
// @enableInferEventHandlers
// @validateRefAccessDuringRender

import {ErrorCategory} from 'babel-plugin-react-compiler/dist/CompilerError';
```
