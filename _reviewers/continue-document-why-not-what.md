---
title: Document why not what
description: 'Documentation should explain rationale and be technically precise. Focus
  on:


  1. Including all required parameters with correct names in examples and documentation'
repository: continuedev/continue
label: Documentation
language: TypeScript
comments_count: 5
repository_stars: 27819
---

Documentation should explain rationale and be technically precise. Focus on:

1. Including all required parameters with correct names in examples and documentation
2. Explaining the reasoning behind code decisions rather than just describing functionality
3. Ensuring technical accuracy in all comments and documentation

Good example:
```typescript
// editor.selectionHighlightBackground is used because it's always 
// partially transparent, which prevents obscuring the selection
// when repurposed here
this.decorationType = vscode.window.createTextEditorDecorationType({
  backgroundColor: new vscode.ThemeColor("editor.selectionHighlightBackground")
});
```

Bad example:
```typescript
// Check if there is a trailing line
// This trims the selection if needed
```

Better example:
```typescript
// If the user selected onto a trailing line but didn't actually include
// any characters in it, they don't want to include that line, so trim it off
```

For API documentation and examples, always verify that parameter names match the actual implementation and all required parameters are included with appropriate descriptions of their purpose.