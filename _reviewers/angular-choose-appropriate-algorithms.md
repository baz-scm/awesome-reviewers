---
title: Choose appropriate algorithms
description: Select algorithms and data structures that match the problem domain and
  access patterns rather than using convenient but suboptimal approaches. For complex
  parsing tasks, use proper AST-based parsing instead of regex. Design data structures
  that align with how data will be accessed and modified.
repository: angular/angular
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 98611
---

Select algorithms and data structures that match the problem domain and access patterns rather than using convenient but suboptimal approaches. For complex parsing tasks, use proper AST-based parsing instead of regex. Design data structures that align with how data will be accessed and modified.

For example, when parsing structured expressions:
```typescript
// Avoid regex for complex parsing
const objectLiteralRegex = /^\s*\{\s*([^}]*)\s*\}\s*$/;

// Use AST-based parsing instead
const parsed = new HtmlParser().parse(template, '', {
  tokenizeExpansionForms: true,
  tokenizeBlocks: true,
  preserveLineEndings: true,
});
```

When designing data structures, consider access patterns:
```typescript
// Instead of complex nested mappings
private _hostNodes = new Map<Node, Map<Node, Node[]>>();

// Consider simpler structures that match usage
private _hostNodes = new Map<Node, { insertionPoint: Node; styles: Node[] }>();
```

Create consistent interfaces for strategy patterns to eliminate conditional logic:
```typescript
// Update strategies to share interface with consistent parameters
interface Strategy {
  supports(element: Element): boolean;
  build(element: Element, index?: number): ComponentTreeNode[];
}
```

This approach reduces complexity, improves maintainability, and ensures algorithms scale appropriately with data size and usage patterns.