---
title: Names reflect semantic purpose
description: Identifiers (variables, properties, keys, IDs) should accurately reflect
  their semantic purpose and context. Names should be chosen to clearly communicate
  the meaning and role of the element within its specific context, not just its technical
  type or generic purpose.
repository: RooCodeInc/Roo-Code
label: Naming Conventions
language: TSX
comments_count: 4
repository_stars: 17288
---

Identifiers (variables, properties, keys, IDs) should accurately reflect their semantic purpose and context. Names should be chosen to clearly communicate the meaning and role of the element within its specific context, not just its technical type or generic purpose.

Examples:

```typescript
// Incorrect: Name doesn't match context
const hasCustomTemperature = value !== undefined 
// Correct: Name reflects actual context
const hasCustomMaxContext = value !== undefined

// Incorrect: Generic/mismatched test ID
data-testid="open-tabs-limit-slider"
// Correct: ID reflects component purpose
data-testid="markdown-lineheight-slider"

// Incorrect: Inconsistent API property naming
interface Props {
  apiRequestFailedMessage: string;
  apiReqStreamingFailedMessage: string; // Inconsistent abbreviation
}
// Correct: Consistent naming pattern
interface Props {
  apiRequestFailedMessage: string;
  apiRequestStreamingFailedMessage: string;
}
```

This standard helps maintain code clarity, improves maintainability, and reduces cognitive load by ensuring names accurately represent their purpose within the codebase.