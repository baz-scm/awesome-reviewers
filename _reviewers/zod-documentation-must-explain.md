---
title: Documentation Must Explain
description: 'Ensure inline docs and comments are accurate, clear, and justified:


  - **Match implementation defaults:** If JSDoc mentions “default”, it must reflect
  what the code actually does. If there’s a real default value, document it (e.g.,
  with an `@default` tag).'
repository: colinhacks/zod
label: Documentation
language: TypeScript
comments_count: 4
repository_stars: 42628
---

Ensure inline docs and comments are accurate, clear, and justified:

- **Match implementation defaults:** If JSDoc mentions “default”, it must reflect what the code actually does. If there’s a real default value, document it (e.g., with an `@default` tag).
- **Explain non-obvious concepts:** For API terms or behaviors that may be unfamiliar (e.g., specific encodings), add a brief comment describing what the term means and how it should be interpreted.
- **Justify suppressions:** Any lint/test ignores or other “silence” directives must include a short explanation of why the suppression is necessary and what it’s protecting against.

Example:
```ts
interface Options {
  /** Registry used to look up metadata. */
  metadata?: $ZodRegistry<Record<string, any>>;

  /** Target JSON Schema version.
   * - "draft-2020-12" — Default.
   * - "draft-7"
   */
  target?: "draft-7" | "draft-2020-12";
}

// Clearly document uncommon terms/encodings
get isBase64url() {
  // base64url is a URL-safe variant of base64 encoding ("-" and "_" instead of "+" and "/").
  return !!this._def.checks.find((ch) => ch.kind === "base64url");
}

// Always explain ignore directives
// biome-ignore lint/complexity/noBannedTypes: `{}` is intentionally used here as the empty object type.
type T = {};
```