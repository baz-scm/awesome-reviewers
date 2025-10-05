---
title: Consistent code formatting
description: Maintain consistent formatting and alignment throughout the codebase
  to improve readability and maintainability. This includes proper indentation for
  multi-line constructs, consistent spacing in documentation, and clear structural
  organization.
repository: vadimdemedes/ink
label: Code Style
language: TypeScript
comments_count: 3
repository_stars: 31825
---

Maintain consistent formatting and alignment throughout the codebase to improve readability and maintainability. This includes proper indentation for multi-line constructs, consistent spacing in documentation, and clear structural organization.

Key formatting practices:
- Use consistent indentation for multi-line type intersections and complex structures
- Align related elements properly for visual clarity
- Format JSDoc comments with proper spacing and include relevant tags like `@default`
- Prefer simpler conditional structures (separate `if` statements over `else if` chains when conditions are mutually exclusive)

Example of proper multi-line type formatting:
```typescript
export type Styles = PaddingStyles &
	MarginStyles &
	FlexStyles &
	DimensionStyles &
	PositionStyles &
	WrapTextStyles;
```

Example of proper JSDoc formatting:
```typescript
/**
 * Set this property to `hidden` to hide content overflowing the box.
 *
 * @default 'visible'
 */
```

This approach ensures code is visually consistent, easier to scan, and more maintainable across the entire codebase.