---
title: meaningful test assertions
description: Write tests that verify specific behavior and outcomes rather than relying
  on weak assertions like snapshots or generic checks. Tests should validate the actual
  functionality being tested, not just capture output or run without proper verification.
repository: cypress-io/cypress
label: Testing
language: TypeScript
comments_count: 4
repository_stars: 48850
---

Write tests that verify specific behavior and outcomes rather than relying on weak assertions like snapshots or generic checks. Tests should validate the actual functionality being tested, not just capture output or run without proper verification.

Instead of snapshot tests that become non-deterministic and don't validate real behavior:
```typescript
// Avoid: Weak snapshot testing
cy.findByTestId('file-match-indicator').should('exist')
```

Write tests with specific, meaningful assertions:
```typescript
// Prefer: Specific behavior verification  
cy.findByTestId('file-match-indicator').should('contain', '2 Matches')
cy.findByRole('link', { name: 'Okay, run the spec' })
  .should('have.attr', 'href', '#/specs/runner?file=src/App.cy.jsx')
```

When adding test coverage, ensure tests verify the expected functionality rather than just exercising code paths. Include assertions that validate the actual behavior users would experience, such as checking that clicking a component correctly finds matches or that spec generation produces the expected output files.

This approach creates more reliable, maintainable tests that catch real regressions and provide confidence in the system's behavior.