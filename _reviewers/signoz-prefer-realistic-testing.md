---
title: Prefer realistic testing
description: Write tests that closely mirror real user interactions and application
  behavior rather than relying on artificial test-specific constructs. This approach
  creates more robust and maintainable tests.
repository: SigNoz/signoz
label: Testing
language: TSX
comments_count: 2
repository_stars: 23369
---

Write tests that closely mirror real user interactions and application behavior rather than relying on artificial test-specific constructs. This approach creates more robust and maintainable tests.

**Key practices:**

1. **Use semantic queries over test IDs**: Prefer `getByRole`, `getByLabelText`, `getByText` instead of `data-testid` attributes. These queries align with how users actually interact with the UI and make tests more resilient to implementation changes.

2. **Use MSW for API testing**: When testing components that fetch data via hooks, use Mock Service Worker (MSW) instead of directly mocking the hooks. This ensures the complete render cycle is tested and maintains realistic data flow.

**Example:**
```tsx
// ❌ Avoid: Artificial test constructs
<div data-testid="funnel-graph-legend-column">
  {/* content */}
</div>

// Test
expect(getByTestId('funnel-graph-legend-column')).toBeInTheDocument();

// ❌ Avoid: Direct hook mocking
jest.mock('hooks/queryBuilder/useGetAggregateKeys', () => ({
  useGetAggregateKeys: jest.fn().mockReturnValue(mockData)
}));

// ✅ Prefer: Semantic queries
<div role="region" aria-label="Funnel graph legend">
  {/* content */}
</div>

// Test
expect(getByRole('region', { name: 'Funnel graph legend' })).toBeInTheDocument();

// ✅ Prefer: MSW for API mocking
// Set up MSW handlers to intercept actual API calls
```

This approach reduces production bundle size by avoiding test-specific attributes and creates tests that break when user experience is actually impacted, not just when implementation details change.