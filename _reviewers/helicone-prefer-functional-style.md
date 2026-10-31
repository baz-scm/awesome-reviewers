---
title: Prefer functional style
description: Favor functional, immutable patterns over imperative mutation and control
  flow. Avoid pushing into arrays or mutating variables in loops; use `map`, `filter`,
  `reduce`, `some`, and `every` instead, keeping variables `const` wherever possible.
  Similarly, avoid multi-branch `switch` statements scattered inline—TypeScript's
  switch lacks the safety of pattern...
repository: Helicone/helicone
label: Code Style
language: TypeScript
comments_count: 4
repository_stars: 6248
---

Favor functional, immutable patterns over imperative mutation and control flow. Avoid pushing into arrays or mutating variables in loops; use `map`, `filter`, `reduce`, `some`, and `every` instead, keeping variables `const` wherever possible. Similarly, avoid multi-branch `switch` statements scattered inline—TypeScript's switch lacks the safety of pattern matching in languages like Rust, so if a switch is necessary, extract it into a small helper function that uses early `return`s instead of `break`s.

For example, instead of:
```ts
const schema: ClickHouseTableSchema[] = [];
for (const table_name of CLICKHOUSE_TABLES) {
  // ...
  schema.push({ table_name, columns: [...] });
}
```
prefer:
```ts
const schema = CLICKHOUSE_TABLES.map((table_name) => ({
  table_name,
  columns: [...],
}));
```

And for building complex strings/URLs with multiple conditional replacements, prefer a `reduce` over sequential mutation:
```ts
const processedUrl = replacements.reduce(
  (url, { placeholder, value }) => (value ? url.replace(placeholder, value) : url),
  config.baseUrl
);
```

This style reduces the risk of subtle bugs from shared mutable state, makes data flow easier to trace, and keeps functions concise. It also naturally simplifies logic—often eliminating the need for separate helper functions (e.g., redundant parsing/counting helpers) once the core operation is expressed functionally.