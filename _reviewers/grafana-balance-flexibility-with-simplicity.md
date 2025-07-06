---
title: Balance flexibility with simplicity
description: When designing component APIs, strive to find the optimal balance between
  providing flexible configuration options and maintaining simplicity. Start with
  essential functionality before adding complex features that may complicate the API
  surface.
repository: grafana/grafana
label: API
language: TSX
comments_count: 2
repository_stars: 68825
---

When designing component APIs, strive to find the optimal balance between providing flexible configuration options and maintaining simplicity. Start with essential functionality before adding complex features that may complicate the API surface.

In Discussion 0, we see how a PillCell component initially had a simpler color implementation:
```typescript
// Simple approach first
function getPillColor(pill: string, cellOptions: TableCellRendererProps['cellOptions']): string {
  if (!isPillCellOptions(cellOptions)) {
    return getDeterministicColor(pill);
  }
  
  const colorMode = cellOptions.colorMode || 'auto';

  // Fixed color mode (highest priority)
  if (colorMode === 'fixed' && cellOptions.color) {
    // Simple implementation
  }
}
```

The team later added more sophisticated key-value mapping for colors when there was clear need, rather than over-complicating the initial implementation.

Similarly, in Discussion 3, a field selection API became overly complex when trying to handle all edge cases:
"When the names collide choosing the correct field from the correct dataframe could be problematic."

Consider these principles when designing APIs:
1. Start with the most common use cases and minimal configuration
2. Add complexity incrementally based on validated user needs
3. When adding flexibility, ensure it doesn't obscure the primary use case
4. Document the recommended approach for simple scenarios

This approach prevents premature complexity while ensuring your API can evolve to meet genuine requirements.