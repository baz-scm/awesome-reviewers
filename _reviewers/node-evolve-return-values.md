---
title: Evolve return values
description: When extending APIs with new capabilities, carefully consider how changes
  to return values affect consumers. Avoid creating polymorphic return types based
  on input options as this reduces predictability and makes it difficult to programmatically
  detect supported features.
repository: nodejs/node
label: API
language: Markdown
comments_count: 8
repository_stars: 112178
---

When extending APIs with new capabilities, carefully consider how changes to return values affect consumers. Avoid creating polymorphic return types based on input options as this reduces predictability and makes it difficult to programmatically detect supported features.

Instead, follow these patterns:

1. For APIs already returning objects:
   - Extend the existing object with new capabilities (e.g., adding `Symbol.dispose`)
   - Maintain backward compatibility by preserving all existing properties

2. For APIs returning primitives or immutable types:
   - Create a new, distinctly named API variant (e.g., `mkdtemp` → `mkdtempDisposable`)
   - Return an object that includes both the original value and the new capability
   - Clearly document the relationship between the original and new APIs

```js
// AVOID: Polymorphic returns based on options
function createTempDir(prefix, { disposable = false } = {}) {
  const path = makeTempDir(prefix);
  return disposable ? 
    { path, [Symbol.dispose]: () => removeTempDir(path) } : 
    path;
}

// BETTER: Separate, clearly named APIs
function createTempDir(prefix) {
  return makeTempDir(prefix);
}

function createDisposableTempDir(prefix) {
  const path = makeTempDir(prefix);
  return {
    path,
    [Symbol.dispose]: () => removeTempDir(path)
  };
}
```

When introducing new return types:
- Document all properties and methods comprehensively
- Consider using named interfaces/types even for anonymous objects to improve API discoverability
- Ensure new capabilities (like disposable resources) follow established patterns and best practices for the feature