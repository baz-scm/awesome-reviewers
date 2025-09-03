---
title: Choose hooks wisely
description: Use React hooks only when you need reactivity and component re-rendering.
  For accessing instantaneous values or one-time data retrieval, prefer plain functions
  to avoid unnecessary re-renders and improve performance.
repository: lobehub/lobe-chat
label: React
language: TypeScript
comments_count: 2
repository_stars: 65138
---

Use React hooks only when you need reactivity and component re-rendering. For accessing instantaneous values or one-time data retrieval, prefer plain functions to avoid unnecessary re-renders and improve performance.

When you only need current state values without subscribing to changes, use direct selector calls instead of hooks:

```typescript
// ❌ Avoid - causes unnecessary re-renders for instantaneous values
export const useMainInterfaceAnalytics = (): MainInterfaceAnalyticsData => {
  const session = useSessionStore(sessionSelectors.currentSession);
  // ... other hook calls
}

// ✅ Prefer - direct access for one-time values
export const getMainInterfaceAnalytics = (): MainInterfaceAnalyticsData => {
  const session = sessionSelectors.currentSession(getSessionStoreState());
  // ... direct selector calls
}
```

Consider component lifecycle when deciding state placement. If components unmount and remount frequently, evaluate whether state should persist in a global store or reset with component lifecycle.