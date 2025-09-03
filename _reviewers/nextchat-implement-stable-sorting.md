---
title: Implement stable sorting
description: When implementing sorting algorithms for collections, ensure stable and
  predictable ordering to avoid inconsistencies from operations like Object.values().
  Use multi-level sorting criteria and consider sequence-based approaches for complex
  ordering requirements.
repository: ChatGPTNextWeb/NextChat
label: Algorithms
language: TypeScript
comments_count: 2
repository_stars: 85721
---

When implementing sorting algorithms for collections, ensure stable and predictable ordering to avoid inconsistencies from operations like Object.values(). Use multi-level sorting criteria and consider sequence-based approaches for complex ordering requirements.

Key principles:
1. **Avoid unstable ordering**: Don't rely on Object.values() or similar operations that may produce inconsistent results across different executions
2. **Implement multi-level sorting**: First sort by primary criteria (e.g., custom vs default), then by secondary criteria (e.g., alphabetical order)
3. **Use sequence numbers for stability**: When complex ordering is needed, assign explicit sequence numbers to ensure consistent results

Example implementation:
```ts
const sortModelTable = (
  models: ReturnType<typeof collectModels>,
  rule: "custom-first" | "default-first",
) =>
  models.sort((a, b) => {
    // Primary sort: custom vs default
    let aIsCustom = a.provider?.providerType === "custom";
    let bIsCustom = b.provider?.providerType === "custom";
    
    if (aIsCustom !== bIsCustom) {
      return aIsCustom === (rule === "custom-first") ? -1 : 1;
    }
    
    // Secondary sort: by provider type, then model name
    if (a.provider && b.provider) {
      const providerTypeComparison = a.provider.providerType.localeCompare(b.provider.providerType);
      if (providerTypeComparison !== 0) {
        return providerTypeComparison;
      }
      return a.name.localeCompare(b.name);
    }
    
    return a.name.localeCompare(b.name);
  });
```

For even more stability, use explicit sequence numbers:
```ts
// Assign sequence numbers for predictable ordering
let customSeq = -1000; // Custom models get negative numbers (higher priority)
let defaultSeq = 1000;  // Default models get positive numbers

const modelWithSorted = {
  ...model,
  sorted: isCustom ? customSeq++ : defaultSeq++
};
```

This approach ensures consistent ordering regardless of the underlying data structure's iteration order and provides clear, maintainable sorting logic.