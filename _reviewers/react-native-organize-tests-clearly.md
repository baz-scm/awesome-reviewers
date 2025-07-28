---
title: organize tests clearly
description: Structure tests with clear organization, focused scope, and minimal duplication
  to improve maintainability and debugging. Each test should have a single, well-defined
  purpose that correlates directly to its name. Group related tests using describe
  blocks and extract common setup code to reduce duplication.
repository: facebook/react-native
label: Testing
language: JavaScript
comments_count: 4
repository_stars: 123178
---

Structure tests with clear organization, focused scope, and minimal duplication to improve maintainability and debugging. Each test should have a single, well-defined purpose that correlates directly to its name. Group related tests using describe blocks and extract common setup code to reduce duplication.

Key principles:
- Split complex tests with multiple expectations into smaller, focused test cases
- Use descriptive test names that clearly indicate what is being tested
- Group related tests under describe blocks and remove redundant prefixes from individual test names
- Extract duplicated setup code into beforeEach hooks or shared helper functions
- Ensure each test validates one specific behavior or scenario

Example of improved test organization:

```javascript
// Instead of:
it('OnEndReached should not be called after initial rendering', () => {
  const ITEM_HEIGHT = 100;
  // setup code...
  // test logic...
});

it('OnEndReached should be called once after scrolling', () => {
  const ITEM_HEIGHT = 100; // duplicated
  // same setup code... // duplicated
  // test logic...
});

// Prefer:
describe('onEndReached', () => {
  const ITEM_HEIGHT = 100;
  let component, instance, data, onEndReached;
  
  beforeEach(() => {
    // shared setup code
  });

  it('should not be called after initial rendering', () => {
    // focused test logic only
  });

  it('should be called once after scrolling', () => {
    // focused test logic only
  });
});
```

This approach makes tests easier to understand, debug, and maintain while reducing code duplication and improving test reliability.