---
title: avoid redundant I/O operations
description: Identify and eliminate repeated expensive operations, particularly file
  system access, by implementing caching, batching, or data sharing strategies. When
  the same file or resource is accessed multiple times within a short timeframe, consider
  caching the result or restructuring the code to perform the operation once and reuse
  the data.
repository: cypress-io/cypress
label: Performance Optimization
language: TypeScript
comments_count: 2
repository_stars: 48850
---

Identify and eliminate repeated expensive operations, particularly file system access, by implementing caching, batching, or data sharing strategies. When the same file or resource is accessed multiple times within a short timeframe, consider caching the result or restructuring the code to perform the operation once and reuse the data.

For example, instead of reading the same file multiple times for each test:
```typescript
// Problematic: reads file for each test
export const getStudioDetails = async (fileDetails: FileDetails) => {
  return {
    studioExtended: await wasTestExtended(fileDetails).catch(() => false),
    studioCreated: await wasTestCreated(fileDetails).catch(() => false),
  }
}
```

Consider caching the file content or combining the operations:
```typescript
// Better: read file once and share the data
export const getStudioDetails = async (fileDetails: FileDetails) => {
  const fileContent = await readFileOnce(fileDetails);
  return {
    studioExtended: checkIfExtended(fileContent),
    studioCreated: checkIfCreated(fileContent),
  }
}
```

This is especially critical when operations scale with the number of tests or files, as the performance impact compounds significantly.