---
title: Meaningful and consistent names
description: Use descriptive, accurate identifiers that follow established conventions
  and maintain consistency throughout your codebase. Variables, parameters, and properties
  should clearly indicate their purpose and content.
repository: mui/material-ui
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 96063
---

Use descriptive, accurate identifiers that follow established conventions and maintain consistency throughout your codebase. Variables, parameters, and properties should clearly indicate their purpose and content.

**Guidelines:**

1. **Use descriptive names** that accurately reflect what variables contain:
   ```typescript
   // Bad
   textarea.evaluate((event) => parseFloat(event.style.height));
   
   // Good
   textarea.evaluate((textareaElement) => parseFloat(textareaElement.style.height));
   ```

2. **Follow standard naming patterns** for common operations:
   ```typescript
   // Bad
   demoData.relativeModules.reduce((prev, curr) => ({ ...prev, [curr.name]: curr.content }), {});
   
   // Good
   demoData.relativeModules.reduce((acc, curr) => ({ ...acc, [curr.name]: curr.content }), {});
   ```

3. **Use conventional prop names** in component APIs:
   ```typescript
   // Bad
   interface TabsContextType {
     tabsValue?: TabsProps['value'];
   }
   
   // Good
   interface TabsContextType {
     value?: TabsProps['value'];  // Standard name when paired with onChange
   }
   ```

4. **Maintain consistent terminology** throughout your APIs to avoid confusion, especially with related concepts:
   ```typescript
   // Bad: Mixing terms for the same concept
   renderTags?: (value: Value[], getTagProps: AutocompleteRenderGetTagProps) => React.ReactNode;
   
   // Good: Use consistent terminology
   renderItems?: (value: Value[], getItemProps: AutocompleteRenderGetItemProps) => React.ReactNode;
   ```

5. **Choose names that reflect semantic meaning** rather than just implementation details:
   ```typescript
   // Less clear
   const hiddenSiblings = getHiddenSiblings(container);
   
   // More clear
   const hiddenElements = getHiddenElements(container);
   ```

Consistent naming improves code readability, maintainability, and helps prevent bugs from misinterpreting a variable's purpose.