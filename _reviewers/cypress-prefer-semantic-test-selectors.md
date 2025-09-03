---
title: Prefer semantic test selectors
description: When writing tests, prioritize semantic and accessibility-based selectors
  over data attributes or generic selectors. Use accessible names, roles, and text
  content to select elements, as these selectors validate both functionality and accessibility
  simultaneously.
repository: cypress-io/cypress
label: Testing
language: TSX
comments_count: 3
repository_stars: 48850
---

When writing tests, prioritize semantic and accessibility-based selectors over data attributes or generic selectors. Use accessible names, roles, and text content to select elements, as these selectors validate both functionality and accessibility simultaneously.

**Preferred approach:**
```javascript
// Good - validates both functionality and accessibility
cy.contains('button', 'Choose Editor').click()
cy.findByRole('button', { name: 'Save Settings' }).click()

// Acceptable when semantic selectors aren't sufficient
cy.get('[data-cy="choose-editor"]').click()

// Avoid - fragile and doesn't validate accessibility
cy.get('.btn-primary').click()
cy.get('button').first().click()
```

**Key benefits:**
- Tests fail when accessibility is broken (missing labels, incorrect roles)
- More resilient to styling changes that don't affect functionality
- Self-documenting - tests show expected user-facing behavior
- Encourages better accessibility practices in the codebase

**When to use data selectors:**
- Complex components where semantic selection is ambiguous
- Temporary testing during rapid prototyping (but update later)
- Cases where multiple elements share the same accessible name

Ensure your tests validate meaningful behavior rather than just element presence. A test that only checks if a component renders without validating its actual functionality provides limited value and may give false confidence.