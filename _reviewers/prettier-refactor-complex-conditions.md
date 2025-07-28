---
title: refactor complex conditions
description: Break down complex inline conditions and nested logic into separate,
  well-named functions or simpler expressions to improve code readability and maintainability.
repository: prettier/prettier
label: Code Style
language: JavaScript
comments_count: 9
repository_stars: 50772
---

Break down complex inline conditions and nested logic into separate, well-named functions or simpler expressions to improve code readability and maintainability.

Complex boolean expressions, deeply nested conditionals, and inline logic with multiple concerns should be extracted into helper functions or simplified using more readable patterns. This makes the code easier to understand, test, and modify.

Examples of improvements:

```javascript
// Before: Complex inline condition
return value !== "" && 
  !(value === "\n" && 
    typeof adjacentNodes === "object" && 
    (adjacentNodes?.previous?.kind === "cj-letter" || 
     adjacentNodes?.next?.kind === "cj-letter") && 
    !isSentenceUseCJDividingSpace(path))
  ? isBreakable ? line : " " 
  : isBreakable ? softline : "";

// After: Extracted helper function
if (value !== "" && canBeConvertedToSpace(path, value, adjacentNodes)) {
  return isBreakable ? line : " ";
}
return isBreakable ? softline : "";

function canBeConvertedToSpace(path, value, adjacentNodes) {
  // Clear, focused logic here
}
```

```javascript
// Before: Complex array operations
if (commaGroup.groups.length > 1) {
  for (const group of commaGroup.groups) {
    if (group.value && typeof group.value === "string" && group.value.includes("#{")) {
      // complex logic
      break;
    }
  }
}

// After: Simplified with array methods
if (commaGroup.groups.some(group => 
  typeof group.value === "string" && group.value.includes("#{"))) {
  // simplified logic
}
```

This approach reduces cognitive load, makes code self-documenting through function names, and enables better testing of individual logical components.