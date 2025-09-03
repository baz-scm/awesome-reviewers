---
title: prioritize backward compatibility
description: When evolving APIs, prioritize maintaining backward compatibility over
  enforcing strict design constraints. Teams should choose approaches that allow existing
  code to continue working rather than forcing breaking changes for theoretical purity.
repository: cypress-io/cypress
label: API
language: TSX
comments_count: 2
repository_stars: 48850
---

When evolving APIs, prioritize maintaining backward compatibility over enforcing strict design constraints. Teams should choose approaches that allow existing code to continue working rather than forcing breaking changes for theoretical purity.

This principle applies when:
- Relaxing API constraints to match real-world usage patterns
- Adding new features while supporting existing interfaces
- Choosing between strict enforcement and practical compatibility

For example, when a team discovered their API documentation required strict method chaining but developers commonly used direct calls, they chose to update the documentation to match actual usage rather than enforce the strict requirement:

```typescript
// Instead of forcing this breaking change:
cy.wrap(null).should(() => { /* assertions */ })

// They allowed the existing pattern:
cy.should(() => { /* assertions */ })
```

Similarly, when evolving from single-item to multi-item support, design the API to handle both cases uniformly rather than creating separate modes. Make the new interface accept arrays while treating single items as arrays of one, ensuring existing code continues to work without modification.