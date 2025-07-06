---
title: Sort with clarity
description: 'Ensure sorting functions are named to accurately reflect their behavior
  and implement consistent sorting approaches throughout the codebase. When implementing
  sort operations:'
repository: grafana/grafana
label: Algorithms
language: Go
comments_count: 2
repository_stars: 68825
---

Ensure sorting functions are named to accurately reflect their behavior and implement consistent sorting approaches throughout the codebase. When implementing sort operations:

1. Clearly specify which fields are used for sorting in function names (e.g., `sortByResourceVersion` instead of generic `sortKeys`)
2. Document unexpected sorting behavior, especially when it might affect other fields
3. Align sorting implementations across related components to ensure consistent behavior

Inconsistent or misleadingly named sorting functions can lead to unexpected results and bugs when code evolves. Consider this example:

```go
// Unclear - suggests sorting by all key fields
func sortHistoryKeys(filteredKeys []DataKey, sortAscending bool) {
    // But actually only sorts by ResourceVersion
    sort.Slice(filteredKeys, func(i, j int) bool {
        if sortAscending {
            return filteredKeys[i].ResourceVersion < filteredKeys[j].ResourceVersion
        }
        return filteredKeys[i].ResourceVersion > filteredKeys[j].ResourceVersion
    })
}

// Better - clearly indicates sorting by ResourceVersion
func sortHistoryKeysByResourceVersion(filteredKeys []DataKey, sortAscending bool) {
    sort.Slice(filteredKeys, func(i, j int) bool {
        if sortAscending {
            return filteredKeys[i].ResourceVersion < filteredKeys[j].ResourceVersion
        }
        return filteredKeys[i].ResourceVersion > filteredKeys[j].ResourceVersion
    })
}
```

When multiple components need to sort the same data structures, ensure they use the same sorting logic to prevent inconsistent results across the system.