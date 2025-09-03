---
title: Optimize React architecture
description: Prefer direct hook usage over prop drilling and carefully consider context
  provider placement to maintain clean component architecture. When custom hooks are
  available, use them directly in components rather than passing their values through
  props. For context providers, aim for global placement when possible, but be mindful
  of routing and component...
repository: SigNoz/signoz
label: React
language: TSX
comments_count: 2
repository_stars: 23369
---

Prefer direct hook usage over prop drilling and carefully consider context provider placement to maintain clean component architecture. When custom hooks are available, use them directly in components rather than passing their values through props. For context providers, aim for global placement when possible, but be mindful of routing and component lifecycle implications.

Example of preferred approach:
```tsx
// Instead of prop drilling useTraceActions results
function AttributeActions() {
  const traceActions = useTraceActions(); // Direct hook usage
  // ... component logic
}

// For context providers, prefer global placement when feasible
// In AppRoutes/index.tsx:
<PreferenceContextProvider>
  <Router>
    {/* All routes have access to context */}
  </Router>
</PreferenceContextProvider>
```

This approach reduces unnecessary prop passing, improves component independence, and creates cleaner data flow patterns. However, always test context provider placement changes thoroughly to ensure they don't introduce routing or rendering issues.