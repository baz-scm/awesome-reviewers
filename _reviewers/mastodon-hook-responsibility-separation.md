---
title: Hook responsibility separation
description: 'Keep hooks and components focused on single, well-defined responsibilities
  to maintain clean architecture and avoid mixing concerns.


  When designing hooks, ensure they have a clear, singular purpose. Avoid combining
  unrelated functionality like DOM manipulation with event handling, or complex business
  logic with simple state management. If a hook or...'
repository: mastodon/mastodon
label: React
language: TSX
comments_count: 4
repository_stars: 48691
---

Keep hooks and components focused on single, well-defined responsibilities to maintain clean architecture and avoid mixing concerns.

When designing hooks, ensure they have a clear, singular purpose. Avoid combining unrelated functionality like DOM manipulation with event handling, or complex business logic with simple state management. If a hook or component starts handling multiple distinct concerns, consider splitting it into focused, composable pieces.

For example, instead of extending a click-handling hook to also manipulate the DOM:

```typescript
// Avoid mixing concerns in a single hook
const useLinks = (node, accountId) => {
  // Handles both click events AND DOM manipulation
  useEffect(() => {
    // Click handling logic
    // DOM manipulation logic - different responsibility!
  }, []);
};

// Better: Keep hooks focused
const useLinks = () => {
  // Only handles click events
};

const useHashtagDropdowns = (node, accountId) => {
  // Only handles DOM manipulation for hashtags
};
```

Similarly, avoid prop drilling by moving helper functions closer to where they're used, and keep component wrappers thin by not adding unnecessary event handling logic that belongs in the underlying native elements.

This separation makes code more maintainable, testable, and follows React's compositional patterns.