---
title: consistent highlighting patterns
description: Maintain consistency in syntax highlighting patterns by using appropriate,
  specific scopes and avoiding overly complex or noisy patterns. Follow Helix-specific
  conventions rather than generic tree-sitter patterns.
repository: helix-editor/helix
label: Code Style
language: Other
comments_count: 12
repository_stars: 39026
---

Maintain consistency in syntax highlighting patterns by using appropriate, specific scopes and avoiding overly complex or noisy patterns. Follow Helix-specific conventions rather than generic tree-sitter patterns.

Key guidelines:
- Use specific scopes like `@keyword.control.repeat` instead of generic `@keyword` when appropriate
- Use Helix-specific scopes like `@constant.numeric.integer` instead of generic `@number`
- Avoid overly complex patterns that try to guess highlighting context
- Remove noisy patterns like `(ERROR) @error` that distract during typing
- Use efficient patterns like `#any-of?` for multiple similar matches
- Ensure proper pattern precedence ordering (specific patterns before generic ones)
- Use cross-compatible predicates like `#match?` instead of platform-specific ones like `#lua-match?`

Example of good pattern specificity:
```scm
; Good - specific scopes
[
  "for"
  "while"
] @keyword.control.repeat

[
  "if" 
  "else"
] @keyword.control.conditional

; Avoid - overly generic
[
  "for"
  "while" 
  "if"
  "else"
] @keyword
```

Example of proper precedence:
```scm
; Specific pattern first
((comment) @comment.block.documentation
  (#match? @comment.block.documentation "^//!"))

; Generic pattern second  
(comment) @comment.line
```

This approach ensures highlighting is consistent, follows project conventions, and provides clear visual feedback without being distracting or overly complex.