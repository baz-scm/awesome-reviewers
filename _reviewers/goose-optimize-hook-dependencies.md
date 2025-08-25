---
title: Optimize hook dependencies
description: Understand React's built-in optimizations and avoid unnecessary dependencies
  in hook arrays. React guarantees that state setters maintain referential stability
  across re-renders, so they don't need to be included in dependency arrays. Similarly,
  ref objects themselves don't change - only their `.current` property does, and changes
  to `.current` don't...
repository: block/goose
label: React
language: TSX
comments_count: 3
repository_stars: 19037
---

Understand React's built-in optimizations and avoid unnecessary dependencies in hook arrays. React guarantees that state setters maintain referential stability across re-renders, so they don't need to be included in dependency arrays. Similarly, ref objects themselves don't change - only their `.current` property does, and changes to `.current` don't trigger re-renders, so refs don't need to be in dependency arrays either.

Use `useCallback` when functions are passed to dependency arrays of other hooks, but avoid premature optimization. As one developer noted: "We could have gotten away with keeping this a function re-created on every render... but we'd have to suppress some warnings and potentially invite some future bugs. Using hooks for all of them seemed the right way to go."

Example of proper dependency management:
```tsx
const performSubmit = useCallback(
  (text?: string) => {
    // Function logic here
  },
  [
    allDroppedFiles,
    displayValue,
    handleSubmit,
    // Don't include: setters, refs, or other stable values
  ]
);

useEffect(() => {
  if (recipeAccepted && initialPrompt && messages.length === 0) {
    setDisplayValue(initialPrompt); // setter doesn't need to be in deps
    hasSetRecipePromptRef.current = true; // ref doesn't need to be in deps
  }
}, [recipeAccepted, initialPrompt, messages.length]); // Only include values that actually change
```