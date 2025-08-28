---
title: avoid manual error handling
description: Prefer centralized error handling mechanisms and specialized utilities
  over manual error handling in individual components. Instead of implementing error
  handling logic directly in each function or component, leverage global error handlers
  and purpose-built utilities.
repository: rocicorp/mono
label: Error Handling
language: TSX
comments_count: 2
repository_stars: 2091
---

Prefer centralized error handling mechanisms and specialized utilities over manual error handling in individual components. Instead of implementing error handling logic directly in each function or component, leverage global error handlers and purpose-built utilities.

For centralized handling, use global `onError` handlers rather than manual error handling in each mutator:

```js
// Avoid: Manual error handling in each component
const handleSubmit = async () => {
  const result = z.mutate.issue.create({...});
  const raceResult = await promiseRace([sleep(5000), result.server]);
  if (raceResult === 0) {
    // TODO show toast - manual error handling
  }
};
```

For specific error scenarios, use specialized utilities that provide both static and runtime safety:

```js
// Avoid: Generic error throwing
if (filter === 'crew') {
  // handle crew
} else if (filter === 'creators') {
  // handle creators  
} else {
  throw new Error(`Unknown filter: ${filter}`);
}

// Prefer: Specialized error utilities
if (filter === 'crew') {
  // handle crew
} else if (filter === 'creators') {
  // handle creators
} else {
  unreachable(filter); // Provides static and runtime assertion
}
```

This approach reduces code duplication, improves consistency, and provides better type safety and debugging capabilities.