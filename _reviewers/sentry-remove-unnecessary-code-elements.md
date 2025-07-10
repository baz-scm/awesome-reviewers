---
title: Remove unnecessary code elements
description: 'Keep code clean and maintainable by removing unnecessary elements. This
  includes:


  1. Omit type annotations when TypeScript can infer them:

  ```typescript'
repository: getsentry/sentry
label: Code Style
language: TSX
comments_count: 5
repository_stars: 41297
---

Keep code clean and maintainable by removing unnecessary elements. This includes:

1. Omit type annotations when TypeScript can infer them:
```typescript
// Bad
const cell: React.ReactNode = renderTableHeadCell?.(column, _columnIndex);

// Good
const cell = renderTableHeadCell?.(column, _columnIndex);
```

2. Remove unnecessary Fragment wrappers when there's only one child:
```typescript
// Bad
<Fragment>
  <WizardInstructionParagraph>
    {content}
  </WizardInstructionParagraph>
</Fragment>

// Good
<WizardInstructionParagraph>
  {content}
</WizardInstructionParagraph>
```

3. Use consistent styling patterns - avoid mixing inline styles with styled components:
```typescript
// Bad
<LoadingIndicator style={{margin: 0, marginTop: space(0.5)}} />

// Good
const StyledLoadingIndicator = styled(LoadingIndicator)`
  margin: ${space(0.5)} 0 0 0;
`;
```

Following these practices improves code readability and maintains consistent patterns across the codebase.