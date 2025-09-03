---
title: Use descriptive names
description: Variable and function names should clearly communicate their actual purpose
  and behavior, not just their initial intent. Avoid vague or misleading names that
  don't accurately reflect what the code does.
repository: SigNoz/signoz
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 23369
---

Variable and function names should clearly communicate their actual purpose and behavior, not just their initial intent. Avoid vague or misleading names that don't accurately reflect what the code does.

When naming variables and functions, consider:
- What the variable/function actually does in practice
- How other developers will interpret the name
- Whether the name accurately describes the behavior throughout the code's lifecycle

Example of problematic naming:
```typescript
// Misleading - suggests it's only used for initialization
const initialValue = getDefaultValue();

// Better - clearly indicates it's used for resets
const defaultValue = getDefaultValue();

// Vague - doesn't explain what data type operation this performs  
export const getDataType = (dataType?: string): DataTypes => {
  // implementation
}

// Better - specific about the conversion/mapping being performed
const mapStringToDataType = (dataType?: string): DataTypes => {
  // implementation  
}
```

Names should serve as documentation for future maintainers, making the code's intent immediately clear without requiring deep analysis of the implementation.