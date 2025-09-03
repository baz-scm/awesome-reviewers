---
title: Extract reusable components
description: Eliminate code duplication by extracting common functionality into shared
  utilities, constants, and base classes. When you notice repeated code patterns,
  logic, or constants across multiple files, consolidate them into reusable components.
repository: novuhq/novu
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 37700
---

Eliminate code duplication by extracting common functionality into shared utilities, constants, and base classes. When you notice repeated code patterns, logic, or constants across multiple files, consolidate them into reusable components.

Key practices:
- Extract common classes into separate files (like BaseHandler for shared method overrides)
- Replace hardcoded values with shared constants (use LAYOUT_PREVIEW_CONTENT_PLACEHOLDER instead of inline HTML strings)
- Centralize logic into single functions (consolidate variable extraction into one place)
- Move parsing and utility functions to dedicated utility files
- Create shared DTOs and validation schemas to avoid duplication

Example:
```typescript
// Before: Duplicated HTML template
const contentPlaceholder = '<div style="border: 1px dashed #E1E4EA;">...</div>';

// After: Shared constant
import { LAYOUT_PREVIEW_CONTENT_PLACEHOLDER } from '@novu/shared';
return body?.replace(regex, LAYOUT_PREVIEW_CONTENT_PLACEHOLDER);
```

This approach improves maintainability, reduces bugs from inconsistent implementations, and makes future changes easier by having a single source of truth.