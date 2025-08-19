---
title: API consistency and decoupling
description: APIs should maintain consistent behavior and avoid tight coupling to
  implementation details or environmental dependencies. Don't make API methods conditionally
  available based on state, and avoid exposing filesystem paths or other environment-specific
  concerns in component interfaces.
repository: microsoft/playwright
label: API
language: TSX
comments_count: 2
repository_stars: 76113
---

APIs should maintain consistent behavior and avoid tight coupling to implementation details or environmental dependencies. Don't make API methods conditionally available based on state, and avoid exposing filesystem paths or other environment-specific concerns in component interfaces.

Instead of conditional API availability:
```typescript
// Avoid: API becomes undefined based on conditions
{onCancel ? (
  <button onClick={onCancel}>Cancel</button>
) : null}
```

Use explicit state checks:
```typescript
// Prefer: Explicit state checking with consistent API
{conversation.isSending() ? (
  <button onClick={onCancel}>Cancel</button>
) : null}
```

Instead of tight coupling to filesystem:
```typescript
// Avoid: Component knows about rootDir and filesystem
const TestResultView = ({ test, result, rootDir }) => {
  // Component fetches files using rootDir
}
```

Decouple by pre-fetching data:
```typescript
// Prefer: Include data explicitly, making component portable
const TestResultView = ({ test, result, preloadedSources }) => {
  // Component works with provided data, no filesystem knowledge
}
```

This approach makes APIs more predictable, testable, and portable across different environments.