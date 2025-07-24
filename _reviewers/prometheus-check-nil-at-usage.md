---
title: Check nil at usage
description: Perform null and validity checks at the point where values are actually
  used, rather than defensively initializing or checking everywhere. This approach
  reduces unnecessary overhead while ensuring safety where it matters most.
repository: prometheus/prometheus
label: Null Handling
language: Go
comments_count: 4
repository_stars: 59616
---

Perform null and validity checks at the point where values are actually used, rather than defensively initializing or checking everywhere. This approach reduces unnecessary overhead while ensuring safety where it matters most.

When handling potentially null or invalid values:
- Check for nil/invalid conditions immediately before use, not during initialization
- Set variables to safe default values (like nil) when errors occur during parsing or initialization
- Validate parameters and bounds before array access or operations that could panic

Example from the codebase:
```go
// Instead of defensive initialization:
if hints == nil {
    hints = &storage.LabelHints{}
}

// Check at point of use:
func someFunction(hints *storage.LabelHints) {
    if hints != nil {
        // use hints safely
    }
}

// Set to safe value on error:
var alertsByRule map[uint64][]*Alert
err = json.NewDecoder(file).Decode(&alertsByRule)
if err != nil {
    alertsByRule = nil  // Set to safe value
    return
}
```

This pattern prevents unnecessary allocations, makes the code's intent clearer, and ensures safety exactly where needed without over-engineering defensive checks throughout the codebase.