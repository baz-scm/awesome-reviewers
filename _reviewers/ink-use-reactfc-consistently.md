---
title: Use React.FC consistently
description: Use React.FC (or React.FunctionComponent) for typing functional components
  instead of verbose function type definitions. React.FC provides built-in typing
  for common props like children, key, and ref, reducing boilerplate and ensuring
  consistency across the codebase.
repository: vadimdemedes/ink
label: React
language: TSX
comments_count: 2
repository_stars: 31825
---

Use React.FC (or React.FunctionComponent) for typing functional components instead of verbose function type definitions. React.FC provides built-in typing for common props like children, key, and ref, reducing boilerplate and ensuring consistency across the codebase.

Instead of verbose function signatures:
```tsx
const UserInput: (props: { test: string }) => JSX.Element | null = ({test}) => {
  // component logic
};
```

Use React.FC for cleaner, more maintainable type definitions:
```tsx
const UserInput: React.FC<{ test: string }> = ({test}) => {
  // component logic
};
```

When children are required (not optional), include them explicitly in your props interface rather than relying on React.FC's optional children:
```tsx
interface ColorProps {
  color: string;
  children: ReactNode; // explicit when required
}

const Color: React.FC<ColorProps> = ({color, children}) => {
  // component logic
};
```

This approach provides better TypeScript integration, clearer component contracts, and leverages React's built-in type definitions effectively.