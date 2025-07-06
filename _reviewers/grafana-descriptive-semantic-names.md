---
title: Descriptive semantic names
description: Always use descriptive variable, parameter, function, and constant names
  that clearly convey their purpose and behavior. Avoid single-letter variables or
  abbreviations except in well-established contexts like loop counters.
repository: grafana/grafana
label: Naming Conventions
language: TSX
comments_count: 6
repository_stars: 68825
---

Always use descriptive variable, parameter, function, and constant names that clearly convey their purpose and behavior. Avoid single-letter variables or abbreviations except in well-established contexts like loop counters.

**Why?**
- Descriptive names make code self-documenting and easier to understand
- They reduce the cognitive load when reading and reviewing code
- They make the codebase more maintainable by future developers
- They help prevent misuse of functions or parameters

**Examples:**

❌ Poor naming:
```typescript
const s = this.selection.value;
if (s) {
  for (let c of this.state) {
    if (c.source === s.source && c.index === s.index) {
      this.selection.next(c);
      break;
    }
  }
}
```

✅ Good naming:
```typescript
const selection = this.selection.value;
if (selection) {
  for (let connection of this.state) {
    if (connection.source === selection.source && connection.index === selection.index) {
      this.selection.next(connection);
      break;
    }
  }
}
```

When naming similar functions, ensure the names clearly differentiate their behaviors:

```typescript
// Names clearly indicate different purposes
shouldLoadPluginInFrontendSandbox()  // Performs HTTP calls and checks
isPluginFrontendSandboxEligible()    // Performs faster local checks
```

For UI elements and parameters that might conflict in shared namespaces, use prefixing conventions:
- Use descriptive category names like "Node field name overrides" instead of generic "Node names"
- Prefix URL parameters with double underscores (e.g., `__returnToTitle`) to avoid conflicts

When temporarily versioning methods (e.g., with numeric suffixes), document when and how they will be renamed:
```typescript
// TODO: Remove the '2' suffix after the feature flag is removed
applyLayoutStylesToDiv2() { ... }
```