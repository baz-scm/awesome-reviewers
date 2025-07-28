---
title: Angular syntax parsing
description: When implementing Angular syntax parsing, ensure robust handling of Angular-specific
  constructs by properly distinguishing AST node types and normalizing flexible syntax
  patterns.
repository: prettier/prettier
label: Angular
language: JavaScript
comments_count: 2
repository_stars: 50772
---

When implementing Angular syntax parsing, ensure robust handling of Angular-specific constructs by properly distinguishing AST node types and normalizing flexible syntax patterns.

For AST visitor keys, only include actual Node objects, not primitive values:
```javascript
// Correct - empty array since name and value are strings, not nodes
angularLetDeclaration: [],

// Incorrect - includes non-node primitives
angularLetDeclaration: ["name", "value"],
```

For Angular control flow blocks, normalize whitespace in block names to handle flexible syntax:
```javascript
// Should handle both:
@else if () {}        // standard spacing
@else   if () {}      // flexible whitespace

// Implementation should normalize "else   if" → "else if"
```

This ensures the parser correctly processes Angular's flexible syntax while maintaining proper AST structure for tooling compatibility.