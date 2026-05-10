---
title: Consistent Readability Rules
description: 'Code should be readable and consistent: avoid inline “magic” expressions,
  prefer named values/helpers, and use uniform style primitives.


  Apply:

  - Replace inline calculations with a named variable/helper when the expression is
  meaningful or potentially repeated:'
repository: mermaid-js/mermaid
label: Code Style
language: Other
comments_count: 8
repository_stars: 87952
---

Code should be readable and consistent: avoid inline “magic” expressions, prefer named values/helpers, and use uniform style primitives.

Apply:
- Replace inline calculations with a named variable/helper when the expression is meaningful or potentially repeated:
  ```js
  const lastEdgeIndex = yy.getEdges().length - 1;
  $$ = $LINKSTYLE;
  yy.updateLink([lastEdgeIndex], $stylesOpt);
  ```
- Prefer consistent layout/style primitives over ad-hoc spacing classes (e.g., use flex `gap-*` instead of mixing `mr-*`, `mb-*`):
  ```vue
  <li v-for="{ iconUrl, featureName } in column" :key="featureName" class="flex gap-2 items-center">
    <img :src="iconUrl" :alt="featureName" class="inline-block h-5 w-5" />
    <span>{{ featureName }}</span>
  </li>
  ```
- Keep syntax and typing consistent (e.g., avoid unnecessary token quoting in grammars; align TS/ref typings across related structures).
- In scripts, use safe quoting/argument handling consistently (prefer arrays + `"${args[@]}"` for pass-through arguments).
- Remove unused grammar/lexer states or keep only what’s actively used; maintain logical rule ordering where it improves scanability.