---
title: Avoid reactive over-engineering
description: Choose the simplest React primitive that meets your requirements rather
  than reaching for complex reactive patterns. Avoid useEffect when useState, useMemo,
  or useCallback would suffice. If you find yourself using useEffect to copy data
  from one state to another state, it's a sign you should restructure your component's
  state management.
repository: angular/angular
label: React
language: Markdown
comments_count: 4
repository_stars: 98611
---

Choose the simplest React primitive that meets your requirements rather than reaching for complex reactive patterns. Avoid useEffect when useState, useMemo, or useCallback would suffice. If you find yourself using useEffect to copy data from one state to another state, it's a sign you should restructure your component's state management.

Prefer direct approaches over unnecessary reactive complexity:
- Use useState for simple state management
- Use useMemo for derived values instead of useEffect + useState
- Use useCallback for stable function references instead of useEffect dependencies
- Reserve useEffect for true side effects like API calls, DOM manipulation, or cleanup

Example of over-engineering:
```jsx
// Avoid: Using useEffect to derive state
const [count, setCount] = useState(0);
const [doubledCount, setDoubledCount] = useState(0);

useEffect(() => {
  setDoubledCount(count * 2);
}, [count]);

// Prefer: Using useMemo for derived values
const [count, setCount] = useState(0);
const doubledCount = useMemo(() => count * 2, [count]);
```

This approach reduces complexity, improves performance, and makes component logic more predictable and easier to debug.