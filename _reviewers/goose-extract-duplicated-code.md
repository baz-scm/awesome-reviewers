---
title: extract duplicated code
description: Identify and eliminate code duplication by extracting shared logic into
  reusable functions, components, or type definitions. When you notice similar code
  patterns appearing in multiple places, refactor them into a single, well-named abstraction.
repository: block/goose
label: Code Style
language: TSX
comments_count: 3
repository_stars: 19037
---

Identify and eliminate code duplication by extracting shared logic into reusable functions, components, or type definitions. When you notice similar code patterns appearing in multiple places, refactor them into a single, well-named abstraction.

This applies to:
- **Repeated JSX elements**: Extract into variables or components
- **Duplicate type definitions**: Create shared types or interfaces  
- **Similar function logic**: Extract into named utility functions

For example, instead of duplicating JSX:
```tsx
{extensionTooltip ? (
  <TooltipWrapper tooltipContent={extensionTooltip}>
    <span className="ml-[10px]">
      {getToolDescription() || snakeToTitleCase(toolCall.name)}
    </span>
  </TooltipWrapper>
) : (
  <span className="ml-[10px]">
    {getToolDescription() || snakeToTitleCase(toolCall.name)}
  </span>
)}
```

Extract the shared element:
```tsx
const toolLabel = (
  <span className="ml-[10px]">
    {getToolDescription() || snakeToTitleCase(toolCall.name)}
  </span>
);

return extensionTooltip ? (
  <TooltipWrapper tooltipContent={extensionTooltip}>{toolLabel}</TooltipWrapper>
) : (
  toolLabel
);
```

Similarly, extract repeated function calls:
```tsx
// Instead of repeating setMentionPopover(prev => ({ ...prev, isOpen: false }))
const closeMentionPopover = () => {
  setMentionPopover(prev => ({ ...prev, isOpen: false }));
};
```

This improves maintainability, reduces the chance of inconsistencies, and makes the code more readable by giving meaningful names to repeated patterns.