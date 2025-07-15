---
title: Cache expensive operations
description: Identify and cache results of computationally expensive or repetitive
  operations instead of recalculating them multiple times. This includes function
  calls, date object creation, data transformations, and resolved promises.
repository: langfuse/langfuse
label: Performance Optimization
language: TypeScript
comments_count: 7
repository_stars: 13574
---

Identify and cache results of computationally expensive or repetitive operations instead of recalculating them multiple times. This includes function calls, date object creation, data transformations, and resolved promises.

Examples of operations to cache:
1. **Function calls with the same inputs**: Store results of pure functions to avoid redundant processing.
2. **Date objects**: Create timestamp variables once and reuse them when multiple operations need the same time reference.
3. **Data transformations**: Process data once and reuse the transformed result.
4. **Resolved promises**: Store and reuse resolved async results rather than triggering the same async operation multiple times.

```typescript
// Before: Inefficient - recalculating for each prompt
await Promise.all(
  resolvedPrompts.map(async (prompt) =>
    promptChangeEventSourcing(
      await promptService.resolvePrompt(prompt), // Redundant async call
```

```typescript
// After: Efficient - reusing already resolved data
await Promise.all(
  resolvedPrompts.map(async (prompt) =>
    promptChangeEventSourcing(
      prompt, // Using already resolved prompt
```

```typescript
// Before: Inefficient - repeated function call
const maxTemperature = getDefaultAdapterParams(selectedProviderApiKey.adapter).maxTemperature;
const temperature = getDefaultAdapterParams(selectedProviderApiKey.adapter).temperature;
const maxTokens = getDefaultAdapterParams(selectedProviderApiKey.adapter).max_tokens;
```

```typescript
// After: Efficient - computing once and reusing
const adapterParams = getDefaultAdapterParams(selectedProviderApiKey.adapter);
const maxTemperature = adapterParams.maxTemperature;
const temperature = adapterParams.temperature;
const maxTokens = adapterParams.max_tokens;
```

Look for patterns where the same operation is performed repeatedly with the same inputs, especially in loops, map functions, or closely related code blocks.