---
title: Use semantically clear names
description: Names should clearly communicate their actual purpose and be consistent
  across similar contexts. Avoid names that mislead about functionality or create
  confusion about the component's role.
repository: microsoft/playwright
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 76113
---

Names should clearly communicate their actual purpose and be consistent across similar contexts. Avoid names that mislead about functionality or create confusion about the component's role.

When naming components, props, or UI elements, ensure the name accurately reflects what the code does rather than what it might do. For example, if a component handles a single checkbox, don't name it in a way that suggests it handles multiple checkboxes.

Maintain consistency in naming patterns, especially for UI elements. If you show additional text in one context, apply the same pattern consistently rather than making it conditional.

Example of unclear naming:
```tsx
// Misleading - suggests multiple checkboxes but handles one
export const CheckBox: React.FunctionComponent<{
    checkBoxSettings: Check<boolean>[];
}>

// Conditional labeling creates inconsistency  
{isFailed && <span>View Trace</span>}
```

Example of clear naming:
```tsx
// Clear - accurately reflects single checkbox functionality
export const CheckBox: React.FunctionComponent<{
    settings: Check<boolean>;
}>

// Consistent and semantically meaningful
<span>View Failing Trace</span>
```

The goal is to make code self-documenting through meaningful names that eliminate ambiguity about purpose and maintain consistent patterns.