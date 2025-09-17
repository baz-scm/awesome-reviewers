---
title: Minimize hook re-renders
description: 'Design React hooks to minimize unnecessary re-renders by avoiding common
  anti-patterns that cause performance issues.


  **Key principles:**


  1. **Avoid umbrella hooks** - Don''t create hooks that combine multiple responsibilities,
  especially mixing read and write operations. Split them into focused, single-purpose
  hooks.'
repository: twentyhq/twenty
label: React
language: TypeScript
comments_count: 5
repository_stars: 35477
---

Design React hooks to minimize unnecessary re-renders by avoiding common anti-patterns that cause performance issues.

**Key principles:**

1. **Avoid umbrella hooks** - Don't create hooks that combine multiple responsibilities, especially mixing read and write operations. Split them into focused, single-purpose hooks.

2. **Don't return functions from hooks** - Functions returned from hooks create new references on each render, triggering re-renders in consuming components. Instead, use utility functions defined outside React scope or stable callbacks with useRecoilCallback.

3. **Minimize state dependencies** - Use techniques like recoil callbacks with `snapshot` and `set` to avoid taking direct dependencies on state atoms, preventing re-renders when those states update.

4. **Keep action hooks dependency-free** - Hooks that perform actions (like create, update, delete) should typically not subscribe to state changes.

**Example of problematic pattern:**
```typescript
// ❌ Bad: Umbrella hook with functions
export const useBillingPlan = () => {
  const plans = useRecoilValue(plansState);
  
  const getBaseLicensedPrice = (planKey) => {
    // Function creates new reference each render
    return plans.find(p => p.key === planKey);
  };
  
  return { plans, getBaseLicensedPrice };
};
```

**Better approach:**
```typescript
// ✅ Good: Focused hooks with stable returns
export const usePlans = () => useRecoilValue(plansState);

export const useCreateWidget = () => {
  return useRecoilCallback(({ snapshot, set }) => async (widgetData) => {
    // No state dependencies, won't cause re-renders
    const currentWidgets = await snapshot.getPromise(widgetsState);
    set(widgetsState, [...currentWidgets, widgetData]);
  });
};
```