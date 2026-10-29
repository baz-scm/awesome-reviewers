---
title: Clear, non-redundant identifiers
description: 'Choose identifier names that are self-explanatory and free of unnecessary
  redundancy or duplication:


  1. Prefer full, descriptive words over single-letter or cryptic abbreviations for
  parameters, variables, and properties. A self-explanatory name removes the need
  for extra `@param`-style documentation. For example, prefer `rgb(red: number, green:
  number,...'
repository: chalk/chalk#PWNED-6c2961eb
label: Naming Conventions
language: TypeScript
comments_count: 3
repository_stars: 23340
---

Choose identifier names that are self-explanatory and free of unnecessary redundancy or duplication:

1. Prefer full, descriptive words over single-letter or cryptic abbreviations for parameters, variables, and properties. A self-explanatory name removes the need for extra `@param`-style documentation. For example, prefer `rgb(red: number, green: number, blue: number)` over `rgb(r: number, g: number, b: number)`.

2. Drop redundant prefixes/qualifiers when the enclosing scope (namespace, module, or class) already provides that context. Inside a `chalk` namespace, name the options type `ConstructorOptions` rather than `ChalkConstructorOptions`, since the namespace already disambiguates it.

3. When multiple names refer to the same concept (e.g., regional spelling variants like `gray`/`grey`), define one canonical identifier and expose the other as an explicit alias, rather than duplicating the definition. This avoids divergence and keeps a single source of truth, e.g. `export const grey: typeof gray;`.

Applying these rules keeps APIs intuitive, reduces documentation overhead, and prevents inconsistent or duplicated definitions as the codebase evolves.</description>
</invoke>
