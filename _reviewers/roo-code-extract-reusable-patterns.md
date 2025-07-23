---
title: Extract reusable patterns
description: Extract repetitive or complex code into reusable functions, components,
  or custom hooks. This improves code organization, reduces duplication, and enhances
  readability.
repository: RooCodeInc/Roo-Code
label: Code Style
language: TSX
comments_count: 8
repository_stars: 17288
---

Extract repetitive or complex code into reusable functions, components, or custom hooks. This improves code organization, reduces duplication, and enhances readability.

For UI components:
- Move complex rendering logic to dedicated components
- Use higher-order components for cross-cutting concerns

For logic patterns:
- Create custom hooks for stateful logic
- Extract helper functions for complex transformations

Example (Before):
```typescript
// Complex event handling logic embedded in component
const className = primaryButtonText === t("chat:startNewTask.title") && currentTaskItem?.id
  ? "flex-1 mr-[6px]"
  : secondaryButtonText
    ? "flex-1 mr-[6px]"
    : "flex-[2] mr-0";

// Repeated pattern for extracting values from events
const value = (e as unknown as CustomEvent)?.detail?.target?.value || 
              ((e as any).target as HTMLTextAreaElement).value;
```

Example (After):
```typescript
// Helper function for className logic
function getButtonClassName(primaryButtonText, t, currentTaskItem, secondaryButtonText) {
  const showShareButton = primaryButtonText === t("chat:startNewTask.title") && currentTaskItem?.id;
  return showShareButton || secondaryButtonText 
    ? "flex-1 mr-[6px]" 
    : "flex-[2] mr-0";
}

// Reusable event value extractor
function getEventValue(e: React.SyntheticEvent | CustomEvent): string {
  return (e as unknown as CustomEvent)?.detail?.target?.value || 
         ((e as React.ChangeEvent<HTMLTextAreaElement>).target).value;
}
```