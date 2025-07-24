---
title: prefer modern React patterns
description: Favor modern React patterns over legacy approaches to improve code maintainability
  and prepare for future React upgrades. Use functional components with hooks instead
  of class components, and prefer `React.useContext` over the `<Context.Consumer>`
  render prop pattern to reduce JSX nesting and improve readability.
repository: argoproj/argo-cd
label: React
language: TSX
comments_count: 2
repository_stars: 20149
---

Favor modern React patterns over legacy approaches to improve code maintainability and prepare for future React upgrades. Use functional components with hooks instead of class components, and prefer `React.useContext` over the `<Context.Consumer>` render prop pattern to reduce JSX nesting and improve readability.

Legacy patterns like `contextTypes` can become blockers when upgrading React versions, so migrating to modern alternatives should be prioritized. When refactoring, replace class component instance variables with `useRef` for mutable references.

Example transformation:
```tsx
// Instead of this legacy pattern:
<Consumer>
  {ctx => (
    <div>{/* component content */}</div>
  )}
</Consumer>

// Use this modern approach:
const ctx = useContext(Context);
return <div>{/* component content */}</div>;
```

Consider adding linter rules to enforce these patterns consistently across the codebase, such as preferring useContext over Consumer components.