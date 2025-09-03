---
title: Test version compatibility
description: When testing across different versions of dependencies, proactively address
  version compatibility issues to prevent compilation failures and ensure proper behavior
  validation. Use mocking or stubbing techniques to resolve dependency conflicts,
  and explicitly test version-specific behaviors including error messages.
repository: cypress-io/cypress
label: Testing
language: JSX
comments_count: 2
repository_stars: 48850
---

When testing across different versions of dependencies, proactively address version compatibility issues to prevent compilation failures and ensure proper behavior validation. Use mocking or stubbing techniques to resolve dependency conflicts, and explicitly test version-specific behaviors including error messages.

For compilation issues caused by version mismatches, consider using tools like `mock-require` or `proxyquire` to stub incompatible modules:

```javascript
// React 17 test that needs to handle React 18-only dependencies
// import React from 'react'
// Use conditional imports or mocking to handle version conflicts
import { mount } from 'cypress/react17' // version-specific import

// Test version-specific behaviors explicitly
describe('legacy mount behavior', () => {
  it('should provide helpful error message when using wrong version', () => {
    // Test that React18 mount gives appropriate error in React17 environment
  })
})
```

This approach prevents build failures while ensuring comprehensive testing of version-specific functionality and migration scenarios.