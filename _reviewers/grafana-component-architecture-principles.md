---
title: Component architecture principles
description: Extract logic that doesn't render JSX into custom hooks instead of components.
  Components that don't return markup create unnecessary abstraction layers and can
  lead to harder-to-follow data flows.
repository: grafana/grafana
label: React
language: TSX
comments_count: 4
repository_stars: 68825
---

Extract logic that doesn't render JSX into custom hooks instead of components. Components that don't return markup create unnecessary abstraction layers and can lead to harder-to-follow data flows.

When a module only manages state, side effects, or logic without rendering UI elements, implement it as a custom hook:

```jsx
// Instead of this:
export function SessionExpiryMonitor({ warningMinutes = 5 }) {
  const [hasShownWarning, setHasShownWarning] = useState(false);
  
  useEffect(() => {
    // monitoring logic
  }, [warningMinutes, hasShownWarning]);
  
  return null; // No JSX rendered
}

// Prefer this:
export function useSessionExpiryMonitor(warningMinutes = 5) {
  const [hasShownWarning, setHasShownWarning] = useState(false);
  
  useEffect(() => {
    // monitoring logic
  }, [warningMinutes, hasShownWarning]);
}
```

For data-dependent components, split them into container and presentational parts to avoid rendering with stale data. This pattern improves predictability by separating data fetching from rendering.

Additionally, ensure proper state updates when modifying child components. If you update child state in a way that should affect the parent, make sure to update the parent state explicitly:

```jsx
// When modifying a child component's state
sceneGridLayout.setState({
  children: [newGridItem, ...sceneGridLayout.state.children],
});

// Don't forget to update the parent state if needed
this.setState({ body: sceneGridLayout });
```

When handling router state, prefer React-specific hooks like `useLocation` over direct browser API subscriptions, as they better integrate with React's lifecycle and re-rendering mechanisms.