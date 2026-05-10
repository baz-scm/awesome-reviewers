---
title: Prefer Grammar Over Regex
description: Use the language parser/grammar (e.g., Langium/Jison) for diagram syntax
  instead of hand-rolled regex parsing. Regex is allowed only for small, well-bounded
  token-level helpers when (a) it precisely matches the intended grammar slice (e.g.,
  remove only *outer* quotes), (b) it doesn’t destructively change user content or
  semantics, and (c) it preserves...
repository: mermaid-js/mermaid
label: Algorithms
language: TypeScript
comments_count: 7
repository_stars: 87952
---

Use the language parser/grammar (e.g., Langium/Jison) for diagram syntax instead of hand-rolled regex parsing. Regex is allowed only for small, well-bounded token-level helpers when (a) it precisely matches the intended grammar slice (e.g., remove only *outer* quotes), (b) it doesn’t destructively change user content or semantics, and (c) it preserves source positions/ranges by avoiding pre-processing that removes/reflows lines before parsing.

Apply these rules:
- **No “core syntax” regex parsing**: if parsing needs to understand quoting, delimiters, comments/directives, or multi-token constructs, implement it in the `.langium` / grammar layer.
- **No destructive transforms**: transformations like stripping wrappers must not remove inner quotes/apostrophes.
- **Parser-owned comment/directive handling**: handle `%% ...` comments and directives in the parser so AST line/range data stays accurate.
- **Delimiter ownership is explicit**: commas/other delimiters should be represented in grammar structure; avoid regexes that “capture beyond” node/value boundaries.

Example: wrapper-quote removal must be outer-only (not global):
```ts
function stripOuterQuotes(s: string): string {
  const t = s.trim();
  if ((t.startsWith('"') && t.endsWith('"')) || (t.startsWith("'") && t.endsWith("'"))) {
    // remove only the outer quotes
    return t.slice(1, -1);
  }
  return t;
}
```

When you must match with regex (e.g., token-level extraction), keep it narrowly scoped and back it with tests for edge cases (escaped quotes, whitespace variations, delimiter presence, comments).