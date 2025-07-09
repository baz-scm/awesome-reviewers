---
title: Consistent camelCase naming
description: Use camelCase consistently for all property names, method names, and
  configuration options, even when interacting with external APIs that use different
  conventions (like snake_case). This maintains codebase consistency and makes interfaces
  more predictable for developers.
repository: vercel/ai
label: Naming Conventions
language: Other
comments_count: 2
repository_stars: 15590
---

Use camelCase consistently for all property names, method names, and configuration options, even when interacting with external APIs that use different conventions (like snake_case). This maintains codebase consistency and makes interfaces more predictable for developers.

When encountering inconsistencies:
- Fix code to follow camelCase rather than propagating inconsistent naming
- Transform between naming conventions at API boundaries when necessary

```typescript
// INCORRECT: Using external snake_case convention in internal code
const options = {
  file_format: 'mp3',
  timestamp_granularities: ['word']
};

// CORRECT: Maintaining camelCase in internal code
const options = {
  fileFormat: 'mp3',
  timestampGranularities: ['word']
};

// When sending to external API, transform as needed
sendToExternalApi({
  file_format: options.fileFormat,
  timestamp_granularities: options.timestampGranularities
});
```

This approach creates a clear separation between internal naming conventions and external API requirements, leading to more consistent and maintainable code.