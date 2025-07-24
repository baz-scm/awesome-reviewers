---
title: Structure validation algorithms
description: 'When implementing or modifying parsing and validation algorithms, carefully
  consider both the correctness and user experience aspects:


  1. **Preserve structural ordering** in data structures like ASTs when order impacts
  semantics. As noted in discussion #1, "In some cases, like in macro scoping, the
  order is actually important," so field reordering can...'
repository: rust-lang/rust
label: Algorithms
language: Other
comments_count: 6
repository_stars: 105254
---

When implementing or modifying parsing and validation algorithms, carefully consider both the correctness and user experience aspects:

1. **Preserve structural ordering** in data structures like ASTs when order impacts semantics. As noted in discussion #1, "In some cases, like in macro scoping, the order is actually important," so field reordering can introduce subtle bugs that are difficult to track down.

2. **Implement intelligent error recovery** for mismatched delimiters by analyzing the context. For different mismatched delimiters scenarios, determine the most likely error:

```rust
// When suggesting missing delimiters, analyze the surrounding context
// BAD: Generic message for all cases
if 1 < 2 {
    let _a = vec!]; // Just showing "mismatched closing delimiter"
}

// GOOD: Context-aware message
if 1 < 2 {
    let _a = vec!]; // "mismatched closing delimiter, may be missing open `[`"
}
```

3. **Avoid over-suggesting fixes** when multiple interpretations are possible. As mentioned in discussion #8, for constructs like `#![w,)`, the fix could be either `[w,]` or `(w,)` depending on context, so the diagnostic algorithm should avoid suggesting a specific solution when ambiguous.

4. **Track related delimiter errors** by collecting information about unmatched opening delimiters to provide more comprehensive diagnostics, as suggested in discussion #7.

These validation algorithms should prioritize correctness while providing meaningful guidance to developers when errors occur.