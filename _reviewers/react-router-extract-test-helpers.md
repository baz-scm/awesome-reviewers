---
title: Extract test helpers
description: Create reusable helper functions for common test setup patterns to reduce
  duplication and improve maintainability. When you find yourself repeating the same
  mock objects, test data structures, or setup code across multiple tests, extract
  them into shared utilities.
repository: remix-run/react-router
label: Testing
language: TSX
comments_count: 3
repository_stars: 55270
---

Create reusable helper functions for common test setup patterns to reduce duplication and improve maintainability. When you find yourself repeating the same mock objects, test data structures, or setup code across multiple tests, extract them into shared utilities.

This approach provides several benefits:
- Changes to data structures only need to be made in one place
- Tests become more readable and focused on the actual behavior being tested  
- Consistency is maintained across the test suite
- New fields or properties can be added without touching every individual test

For example, instead of duplicating complex mock objects:

```javascript
// Before: Repeated in every test
let context: FrameworkContextObject = {
  routeModules: { root: { default: () => null } },
  manifest: {
    routes: {
      root: {
        hasLoader: false,
        hasAction: false,
        hasErrorBoundary: false,
        id: "root",
        module: "root.js",
      },
    },
    entry: { imports: [], module: "" },
    url: "",
    version: "",
  },
};

// After: Centralized helper
let context = mockFrameworkContext();
```

Similarly, when adding new fields to test data arrays, update all existing entries to maintain consistency, even if the new field has the same value as existing ones. This ensures that assertions against the new field work correctly across all test cases.