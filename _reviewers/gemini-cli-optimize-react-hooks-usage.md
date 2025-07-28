---
title: optimize React hooks usage
description: Avoid useRef unless strictly necessary and ensure useEffect has proper
  dependencies to prevent unnecessary re-renders. useRef makes logic harder to reason
  about and should be replaced with more straightforward patterns when possible. For
  useEffect, extract values outside the effect when they don't need to be dependencies,
  and ensure the dependency array...
repository: google-gemini/gemini-cli
label: React
language: TSX
comments_count: 2
repository_stars: 65062
---

Avoid useRef unless strictly necessary and ensure useEffect has proper dependencies to prevent unnecessary re-renders. useRef makes logic harder to reason about and should be replaced with more straightforward patterns when possible. For useEffect, extract values outside the effect when they don't need to be dependencies, and ensure the dependency array accurately reflects what the effect actually uses.

Example of avoiding useRef:
```tsx
// Instead of using useRef for callbacks
() => toggleVimModeRef.current?.()

// Use a generic function approach
const handleSettingsUpdate = (updateFn) => updateFn();
```

Example of optimizing useEffect:
```tsx
// Extract values that don't need to be dependencies
const prompt = config.getQuestion();
useEffect(() => {
  // Use prompt here
}, [/* proper dependencies only */]);
```

This approach improves code maintainability by making component logic more predictable and reducing unnecessary re-renders that can impact performance.