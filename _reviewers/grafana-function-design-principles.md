---
title: Function design principles
description: 'Design functions for maximum reusability, clarity, and maintainability.
  Follow these principles:


  1. **Pass complete objects instead of extracted properties**: When a function needs
  to extract multiple properties from an object, pass the whole object rather than
  individual properties. This makes the function more composable and easier to reuse
  in different...'
repository: grafana/grafana
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 68825
---

Design functions for maximum reusability, clarity, and maintainability. Follow these principles:

1. **Pass complete objects instead of extracted properties**: When a function needs to extract multiple properties from an object, pass the whole object rather than individual properties. This makes the function more composable and easier to reuse in different contexts.

```typescript
// Avoid
function shouldTextOverflow(
  fieldType: FieldType,
  cellType: TableCellDisplayMode,
  textWrap: boolean,
  cellInspect: boolean
): boolean {
  return fieldType === FieldType.string && cellType !== TableCellDisplayMode.Image && !textWrap && !cellInspect;
}

// Prefer
function shouldTextOverflow(field: Field): boolean {
  const cellType = getCellOptions(field).type;
  const textWrap = shouldTextWrap(field);
  const cellInspect = isCellInspectEnabled(field);
  return field.type === FieldType.string && cellType !== TableCellDisplayMode.Image && !textWrap && !cellInspect;
}
```

2. **Extract reusable functions instead of duplicating code**: When similar code appears in multiple places, extract it into a shared function. Before writing new utility functions, check if similar functionality already exists in the codebase.

3. **Use named functions over anonymous functions**: Replace self-executing anonymous functions with named functions for better readability and debuggability.

```typescript
// Avoid
importPromises[pluginId] = (async () => {
  // implementation
})();

// Prefer
async function loadPlugin(pluginId: string): Promise<AppPlugin> {
  // implementation
}
importPromises[pluginId] = loadPlugin(pluginId);
```

4. **Create purpose-specific functions**: When dealing with complex logic that serves different purposes, create separate purpose-specific functions rather than one complex function with many conditional branches. This improves readability and makes the code easier to maintain.