---
title: Follow React component patterns
description: React components should be rendered as standard JSX elements, not called
  as functions, and should follow established architectural patterns. This ensures
  consistency with React conventions and maintainability.
repository: twentyhq/twenty
label: React
language: TSX
comments_count: 2
repository_stars: 35477
---

React components should be rendered as standard JSX elements, not called as functions, and should follow established architectural patterns. This ensures consistency with React conventions and maintainability.

When you see a component being called as a function like `WorkflowActionMenuItems(props)`, refactor it to proper JSX syntax: `<WorkflowActionMenuItems {...props} />`. Additionally, ensure components have proper data backing and follow established patterns in the codebase.

Example of incorrect usage:
```tsx
{WorkflowActionMenuItems(HUMAN_INPUT_ACTIONS, theme, handleCreateStep)}
```

Example of correct usage:
```tsx
<WorkflowActionMenuItems 
  actions={HUMAN_INPUT_ACTIONS} 
  theme={theme} 
  onCreateStep={handleCreateStep} 
/>
```

This pattern maintains React's declarative nature and ensures components integrate properly with React's rendering system and developer tools.