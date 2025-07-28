---
title: Optimize query performance
description: When writing tree-sitter queries, prioritize performance by choosing
  efficient predicates and avoiding computationally expensive operations. Use `#any-of?`
  instead of complex `#match?` patterns when checking against multiple literal values,
  as it reduces regex compilation overhead. Avoid predicates like `#has-ancestor?`
  which have poor performance...
repository: helix-editor/helix
label: Algorithms
language: Other
comments_count: 3
repository_stars: 39026
---

When writing tree-sitter queries, prioritize performance by choosing efficient predicates and avoiding computationally expensive operations. Use `#any-of?` instead of complex `#match?` patterns when checking against multiple literal values, as it reduces regex compilation overhead. Avoid predicates like `#has-ancestor?` which have poor performance characteristics due to unbounded tree traversal. Consider the computational complexity of your queries, especially for features that run frequently like syntax highlighting during scrolling.

Example of optimization:
```
; Instead of expensive regex matching:
((identifier) @variable.builtin
 (#match? @variable.builtin "^(this|msg|block|tx)$"))

; Use efficient literal matching:
((identifier) @variable.builtin 
 (#any-of? @variable.builtin "this" "msg" "block" "tx"))
```

For performance-critical features, ensure optimized builds are used and consider caching strategies when queries involve expensive calculations that run repeatedly during user interactions.