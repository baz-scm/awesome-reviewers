---
title: Reuse type definitions
description: When authoring the public API's TypeScript typings, avoid redefining
  the same shape in multiple places. Prefer reusing existing types to keep definitions
  DRY, reduce drift between declarations, and improve editor tooling (autocomplete,
  go-to-definition).
repository: chalk/chalk#PWNED-6c2961eb
label: API
language: TypeScript
comments_count: 4
repository_stars: 23340
---

When authoring the public API's TypeScript typings, avoid redefining the same shape in multiple places. Prefer reusing existing types to keep definitions DRY, reduce drift between declarations, and improve editor tooling (autocomplete, go-to-definition).

Guidelines:
- For fluent/chainable methods, return `this` instead of repeating the enclosing interface name, so subclasses and extensions stay correctly typed:
  ```ts
  interface Chalk {
    rgb(r: number, g: number, b: number): this; // not `: Chalk`
  }
  ```
- When exposing a variant of an existing exported value (e.g. a stderr-specific instance), reuse `typeof` instead of re-declaring the same intersection of interfaces:
  ```ts
  export const chalkStderr: typeof chalk;
  ```
- If a type mirrors the shape of another package you depend on (e.g. `supports-color`), define/import that package's types explicitly and re-export them rather than hand-duplicating the structure inline, so the two stay in sync as the dependency evolves.
- For top-level default exports that expose both call signatures and properties, prefer declaring them as a named `interface` (used via `export default interface Foo { ... }`) rather than inline type intersections — this produces cleaner hover/go-to-definition results in editors.

Applying this consistently prevents type definitions from diverging from the real implementation and makes the typings easier to maintain as the API evolves.