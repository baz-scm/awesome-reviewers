---
title: Favor component composition
description: Design components to be configurable through props rather than relying
  on external context like URL paths or modifying shared UI components directly. This
  approach improves reusability, maintainability, and reduces coupling between components
  and their usage contexts.
repository: calcom/cal.com
label: React
language: TSX
comments_count: 3
repository_stars: 37732
---

Design components to be configurable through props rather than relying on external context like URL paths or modifying shared UI components directly. This approach improves reusability, maintainability, and reduces coupling between components and their usage contexts.

Key principles:
1. **Use props for configuration**: Instead of deriving component behavior from routes or global state, pass configuration explicitly through props
2. **Compose rather than modify**: When customizing existing components, use composition patterns (like passing custom components as props) rather than modifying the base component
3. **Reuse existing components**: Before creating new components, check if existing ones can be reused or extended

Example of good composition:
```tsx
// Instead of modifying Select component directly
<Select 
  components={{ 
    Option: CustomOption 
  }} 
  // other props
/>

// Instead of path-based configuration
<BillingCredits 
  teamId={teamId}
  isOrgScoped={isOrgScoped}
/>
```

This pattern makes components more predictable, testable, and easier to refactor when requirements change.