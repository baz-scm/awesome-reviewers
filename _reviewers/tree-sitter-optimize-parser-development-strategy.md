---
title: optimize parser development strategy
description: When developing parsers or grammars, apply strategic optimization by
  prioritizing commonly used language features and choosing appropriate conflict resolution
  algorithms based on performance trade-offs.
repository: tree-sitter/tree-sitter
label: Algorithms
language: Markdown
comments_count: 3
repository_stars: 21799
---

When developing parsers or grammars, apply strategic optimization by prioritizing commonly used language features and choosing appropriate conflict resolution algorithms based on performance trade-offs.

Focus development effort on the most frequently used language constructs rather than attempting comprehensive coverage initially. As noted in parser development practices: "Most languages have a long-tail of features that don't get utilized frequently. It is reasonable to prioritize developing 80% of a language and only supporting commonly used elements."

For handling parsing conflicts, choose resolution strategies based on their computational complexity:

1. **Compile-time optimization**: Rearrange grammar rules, specify associativity/precedence - these resolve ambiguities during parser generation with no runtime cost
2. **Runtime resolution**: Add explicit conflict handling - this defers ambiguity resolution to parse time, potentially impacting performance

Example conflict resolution approaches:
```javascript
// Compile-time: Use precedence to resolve operator conflicts
precedence: [
  ['left', '+', '-'],
  ['left', '*', '/'],
]

// Runtime: Allow parser to handle ambiguity dynamically  
conflicts: $ => [
  [$.expression, $.statement]
]
```

This optimization strategy balances development velocity with parser performance, ensuring efficient resource allocation while maintaining practical functionality for the most common use cases.