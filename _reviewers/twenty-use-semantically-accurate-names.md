---
title: Use semantically accurate names
description: Names should clearly and accurately reflect their actual purpose, functionality,
  and scope. Avoid misleading terminology that doesn't match the component's or variable's
  true behavior.
repository: twentyhq/twenty
label: Naming Conventions
language: TSX
comments_count: 6
repository_stars: 35477
---

Names should clearly and accurately reflect their actual purpose, functionality, and scope. Avoid misleading terminology that doesn't match the component's or variable's true behavior.

Key principles:
- Component names should describe what they actually do, not what they seem to do
- Boolean variables should clearly indicate what condition they represent
- Follow established naming conventions (e.g., "Styled" prefix for styled components)
- Use descriptive constants instead of magic numbers
- Choose parameter names that allow for future extensibility

Examples of improvements:
```typescript
// ❌ Misleading - not for "object options" but "select field options"
ObjectOptionsDropdownCreateNewOption

// ✅ Clear and accurate
AddSelectOptionMenuItem

// ❌ Unclear boolean with double negative
const isPlainString = !streamData.includes('\n') || !streamData.split('\n').some(...)

// ✅ Clear and positive
const hasStructuredStreamData = (data: string): boolean => {
  if (!data.includes('\n')) return false;
  return data.split('\n').some(line => { /* ... */ });
}

// ❌ Missing naming convention
const AddStyleContainer = { /* ... */ }

// ✅ Follows styled component convention  
const StyledAddContainer = { /* ... */ }

// ❌ Single parameter limits extensibility
uniqueNotEditableKey="content-type"

// ✅ Array allows multiple values
readonlyKeys={["content-type"]}
```

This ensures code is self-documenting and reduces cognitive load for developers trying to understand the codebase.