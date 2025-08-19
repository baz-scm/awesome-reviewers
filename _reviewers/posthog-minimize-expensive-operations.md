---
title: minimize expensive operations
description: Avoid triggering expensive operations (queries, API calls, computations)
  on every user input or state change. Instead, use appropriate triggers that balance
  responsiveness with performance.
repository: PostHog/posthog
label: Performance Optimization
language: TSX
comments_count: 2
repository_stars: 28460
---

Avoid triggering expensive operations (queries, API calls, computations) on every user input or state change. Instead, use appropriate triggers that balance responsiveness with performance.

Key strategies:
- Use `onBlur` instead of `onChange` for expensive operations that don't need immediate feedback
- Implement save/submit buttons for complex forms to batch expensive operations
- Move data fetching from `useEffect` to event handlers when the data is only needed in response to specific user actions
- Consider the cost-benefit ratio: "breakdown queries are expensive as is" - defer expensive operations until truly necessary

Example from the discussions:
```tsx
// Instead of triggering expensive queries on every change:
<LemonInput 
  onChange={(value) => expensiveQuery(value)} // Causes UI jumpiness
/>

// Use onBlur or save buttons:
<LemonInput 
  onBlur={(value) => expensiveQuery(value)} // Better performance
/>

// Or move from useEffect to event handlers:
// Instead of:
useEffect(() => {
  if (needsData) {
    fetchExpensiveData()
  }
}, [dependency])

// Use:
const handleUserAction = () => {
  if (needsData) {
    fetchExpensiveData() // Only when actually needed
  }
}
```

This approach reduces unnecessary resource utilization and prevents performance bottlenecks that degrade user experience.