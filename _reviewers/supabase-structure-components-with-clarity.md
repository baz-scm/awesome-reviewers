---
title: Structure components with clarity
description: 'Maintain clean and logical component organization by following these
  guidelines:


  1. Keep related files together - place test files beside their components rather
  than in separate folders'
repository: supabase/supabase
label: Code Style
language: TSX
comments_count: 5
repository_stars: 86070
---

Maintain clean and logical component organization by following these guidelines:

1. Keep related files together - place test files beside their components rather than in separate folders
2. Avoid declaring components within other components - this creates unnecessary coupling and complicates state management
3. Use PropsWithChildren instead of React.FC for typing components
4. Minimize prop drilling by accessing state directly where needed

Example of proper component organization:

```tsx
// ✅ Good: Test file next to component
// components/MyComponent/
//   - MyComponent.tsx
//   - MyComponent.test.tsx

// ✅ Good: Components defined at module level
export const ParentComponent = () => {
  return <ChildComponent />
}

export const ChildComponent = () => {
  return <div>Child</div>
}

// ❌ Bad: Component defined within another
const ParentComponent = () => {
  const NestedComponent = () => { // Avoid this
    return <div>Nested</div>
  }
  return <NestedComponent />
}
```

This organization improves code maintainability, reduces coupling, and makes the codebase easier to navigate.