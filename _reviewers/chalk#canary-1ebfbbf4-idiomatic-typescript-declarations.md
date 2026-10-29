---
title: Idiomatic TypeScript declarations
description: 'When writing `.d.ts` files, keep type declarations minimal, idiomatic,
  and free of duplication. Specifically:


  - If a type already exists in another module, re-export it explicitly (`export {
  Foo, Bar } from ''module''`) instead of redefining it with duplicated documentation.
  Place such re-exports together, typically at the bottom of the file.'
repository: chalk/chalk#CANARY-1ebfbbf4
label: Code Style
language: TypeScript
comments_count: 4
repository_stars: 23342
---

When writing `.d.ts` files, keep type declarations minimal, idiomatic, and free of duplication. Specifically:

- If a type already exists in another module, re-export it explicitly (`export { Foo, Bar } from 'module'`) instead of redefining it with duplicated documentation. Place such re-exports together, typically at the bottom of the file.
- Avoid creating a standalone named interface for a shape that's only used in one place (e.g., an options property); define it inline instead, to keep the public API surface minimal.
- For methods on an interface, use method shorthand syntax rather than arrow-function-style properties:

```ts
// Preferred
interface Chalk {
	rgb(r: number, g: number, b: number): Chalk;
}

// Avoid
interface Chalk {
	rgb: (r: number, g: number, b: number) => Chalk;
}
```

Following these conventions keeps type definitions concise, avoids drift between duplicated docs/types, and matches common TypeScript style guidelines.