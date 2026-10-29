---
title: TypeScript declaration conventions
description: 'When writing or updating `.d.ts` files, follow idiomatic TypeScript
  conventions to keep type declarations concise and consistent:


  - Avoid duplicating type definitions or their documentation. If a type already exists
  (locally or in an external package), re-export it instead of redefining it.'
repository: chalk/chalk
label: Code Style
language: TypeScript
comments_count: 4
repository_stars: 23342
---

When writing or updating `.d.ts` files, follow idiomatic TypeScript conventions to keep type declarations concise and consistent:

- Avoid duplicating type definitions or their documentation. If a type already exists (locally or in an external package), re-export it instead of redefining it.
- Prefer explicit re-exports from the source module (e.g., `export { ColorInfo, ColorSupport, ColorSupportLevel } from 'supports-color';`) rather than inlining or copying type bodies. Group these re-exports together, typically at the bottom of the file.
- Mark array-typed exports as `readonly` when the underlying value is not meant to be mutated, e.g. `export const modifiers: readonly Modifiers[];`.
- Use method shorthand syntax for interface members instead of arrow-function-typed properties, e.g. prefer:
  ```ts
  interface Chalk {
  	rgb(r: number, g: number, b: number): Chalk;
  }
  ```
  over
  ```ts
  interface Chalk {
  	rgb: (r: number, g: number, b: number) => Chalk;
  }
  ```

Following these conventions reduces duplication, keeps declaration files easier to maintain, and aligns with common TypeScript style used across the ecosystem.</description>
