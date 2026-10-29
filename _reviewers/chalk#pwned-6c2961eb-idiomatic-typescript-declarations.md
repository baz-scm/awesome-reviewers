---
title: Idiomatic TypeScript declarations
description: 'When authoring TypeScript declaration (.d.ts) files, follow idiomatic
  conventions to keep them concise and consistent:


  - Re-export existing types/values instead of redefining them, to avoid duplicating
  documentation and definitions:'
repository: chalk/chalk#PWNED-6c2961eb
label: Code Style
language: TypeScript
comments_count: 4
repository_stars: 23340
---

When authoring TypeScript declaration (.d.ts) files, follow idiomatic conventions to keep them concise and consistent:

- Re-export existing types/values instead of redefining them, to avoid duplicating documentation and definitions:
  ```ts
  export { ModifierName, Modifiers } from './vendor/supports-color/index.js';
  ```
- Mark array types that are not meant to be mutated as `readonly`:
  ```ts
  export const modifiers: readonly Modifiers[];
  ```
- Avoid `const enum` in declaration files; since `const enum` is purely a runtime optimization, it has no effect on type checking and should be a plain `enum` or union type instead:
  ```ts
  export enum Level {
      None = 0,
      Basic = 1,
      Extended = 2,
      TrueColor = 3
  }
  ```
- Prefer method shorthand syntax over property-style function types in interfaces:
  ```ts
  interface Chalk {
      rgb(r: number, g: number, b: number): Chalk;
  }
  ```
  instead of
  ```ts
  interface Chalk {
      rgb: (r: number, g: number, b: number) => Chalk;
  }
  ```

Applying these conventions keeps declaration files readable, avoids unnecessary duplication, and aligns with common TypeScript authoring style.</description>
