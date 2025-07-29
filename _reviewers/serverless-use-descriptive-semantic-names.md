---
title: Use descriptive semantic names
description: Variable and function names should clearly communicate their purpose,
  type, and scope without requiring additional context. Avoid confusing naming patterns
  and follow established conventions to improve code readability and maintainability.
repository: serverless/serverless
label: Naming Conventions
language: JavaScript
comments_count: 16
repository_stars: 46810
---

Variable and function names should clearly communicate their purpose, type, and scope without requiring additional context. Avoid confusing naming patterns and follow established conventions to improve code readability and maintainability.

**Key Guidelines:**
- Avoid underscore prefixes/suffixes (`statement_`, `_areMergeablePolicyStatements`) - they suggest private members or temporary variables
- Don't capitalize variables that aren't constructors (`Effect`, `Action`) - capitalization implies class constructors
- Use descriptive names over abbreviations (`serviceDir` instead of `sDir`, `shouldMinify` instead of `minify`)
- Name booleans as questions (`isConsoleDevMode`, `shouldMinify`, `isInteractiveTerminal`)
- Choose semantically accurate names that reflect data type (`kmsKeyArn` for ARN values, `resolvedPath` vs `entryFileRealPath`)
- Maintain consistency across related concepts (`websocket` not `websockets` to match event names)

**Example:**
```javascript
// Avoid
const statement_ = statements.find(el => ...);
const Effect = statement.Effect; // Looks like constructor
const sDir = fixture.servicePath;
const minify = this.options['minify-template'];

// Prefer  
const matchingStatement = statements.find(el => ...);
const effect = statement.Effect; // Clear it's a value
const serviceDir = fixture.servicePath;
const shouldMinify = this.options['minify-template'];
```

Well-chosen names serve as inline documentation, reducing cognitive load and making code self-explanatory to future maintainers.