---
title: Path comparison precision
description: When implementing file path matching or exclusion algorithms, use precise
  comparison techniques that respect directory boundaries rather than simple string
  operations. Naïve prefix matching using `startsWith()` can lead to unexpected behavior
  by accidentally matching unrelated paths that share prefixes.
repository: oven-sh/bun
label: Algorithms
language: TypeScript
comments_count: 2
repository_stars: 79093
---

When implementing file path matching or exclusion algorithms, use precise comparison techniques that respect directory boundaries rather than simple string operations. Naïve prefix matching using `startsWith()` can lead to unexpected behavior by accidentally matching unrelated paths that share prefixes.

For example, with an exclude pattern of `'foo'`, a simple implementation might exclude both `'foo/bar'` (intended) and `'foobar'` (likely unintended).

Instead, implement directory-aware comparisons:

```js
// Incorrect - too inclusive
if (excludeGlobs?.some(([glob, p]) => glob.match(ent) || ent.startsWith(p)))

// Correct - respects directory boundaries
if (excludeGlobs?.some(([glob, p]) => glob.match(ent) || p === ent || ent.startsWith(p + path.sep)))
```

For complex pattern matching like glob implementations, consider both exact matches and proper directory hierarchy to ensure your algorithm behaves predictably across edge cases, especially when handling wildcards or path separators that may differ between operating systems.