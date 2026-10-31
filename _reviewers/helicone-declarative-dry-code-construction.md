---
title: Declarative, DRY code construction
description: 'Favor declarative, immutable patterns over imperative mutation, and
  avoid duplicating literals or string concatenation logic across the codebase.


  - Build arrays/objects declaratively instead of push()-ing into a mutable array.
  Use spreads with conditional expressions so the structure is clear at a glance:'
repository: Helicone/helicone
label: Code Style
language: TSX
comments_count: 3
repository_stars: 6248
---

Favor declarative, immutable patterns over imperative mutation, and avoid duplicating literals or string concatenation logic across the codebase.

- Build arrays/objects declaratively instead of push()-ing into a mutable array. Use spreads with conditional expressions so the structure is clear at a glance:
```ts
const items = [
  ...(role === "assistant" ? [{ label: "Add Tool Call", onClick: addToolCall }] : []),
  ...(role === "user" && onAddText ? [{ label: "Add Text", onClick: onAddText }] : []),
  ...(role === "user" && onAddImage ? [{ label: "Add Image", onClick: onAddImage }] : []),
];
```

- Never hardcode "magic" values (limits, sizes, thresholds) inline, especially when the same value appears in more than one place (e.g., a `500` request limit used in both a hook and a button component). Extract these into a shared `constants.ts` and import them where needed, so the value and its rationale are documented in a single place.

- For conditional className composition, prefer a dedicated utility (e.g., `clsx`) over manual template-literal string concatenation:
```tsx
className={clsx(
  "text-sm font-medium items-center text-gray-900 dark:text-gray-100 hidden sm:flex gap-1",
  textClassName
)}
```

Applying these practices keeps code readable, reduces duplication, and makes future changes (e.g., tuning a limit or adding a class) a single-point edit instead of a search-and-replace across the codebase.