---
title: React Semantics In Optimizations
description: When optimizing React code (including compiler transforms, memo blocks,
  and generated naming), follow React semantics explicitly instead of assuming identity
  or emitting overly-specific identifiers.
repository: facebook/react#b3
label: React
language: Markdown
comments_count: 2
repository_stars: 251883
---

When optimizing React code (including compiler transforms, memo blocks, and generated naming), follow React semantics explicitly instead of assuming identity or emitting overly-specific identifiers.

1) Don’t drop dependency identity for refs/values
- If a memo block depends on a ref (or any value) whose identity may change across renders, keep it in the dependency tracking.
- Only ignore a dependency when you can prove its identity is stable (e.g., a ref created once and never replaced), not based on “it probably won’t change.”

Example (bad assumption: ref identity is always stable):
```js
const customRef = useCustomRef(); // may return a different ref
// ... later, an optimization/memo block treats customRef as constant
```

Safer approach:
- Track `customRef` (or the exact identity used) so the memo block recomputes when that identity changes.

2) Canonicalize built-in hook handling
- For built-in React hooks like `useEffect`, prefer canonical representations (e.g., don’t include unnecessary argument indices like `arg0`) when it’s unambiguous.
- If there are multiple anonymous function arguments requiring disambiguation, then include indices; otherwise omit them for stable, predictable output.

Example rule of thumb:
- `useEffect(() => { ... }, [deps])` → treat the effect callback as the single primary anonymous function argument; avoid extra indexing.
- If a hook call includes multiple anonymous function arguments, keep indices only to disambiguate them.

Apply this consistently in React component code, hook code, and any compiler/transform/generator that creates memo dependencies or names from hook arguments.