---
title: Co-locate related code
description: Place functionally related code and comments together to improve readability
  and maintainability. When code elements interact with the same data structures or
  contribute to the same logical operation, they should be grouped together, even
  if it requires reorganizing existing code.
repository: facebook/react
label: Code Style
language: Javascript
comments_count: 2
repository_stars: 236925
---

Place functionally related code and comments together to improve readability and maintainability. When code elements interact with the same data structures or contribute to the same logical operation, they should be grouped together, even if it requires reorganizing existing code.

Specifically:
- Place comments directly adjacent to the code they describe
- Group operations that affect the same resource or state
- Keep initialization and cleanup code for the same feature together
- When moving code, ensure related comments and operations move with it

Example:
```javascript
// GOOD: Comment and related functionality are co-located
if (__DEV__) {
  // Initialize element properties after blocked references
  const init = initializeElement.bind(null, response, element);
  blockedChunk.then(init, init);
}

// BAD: Related operations are separated
abortListeners.clear();
// ... many lines of unrelated code ...
callOnAllReadyIfReady(request); // Should be next to abortListeners.clear()
```

This approach reduces cognitive load when reading code and decreases the likelihood of bugs when modifying related functionality.