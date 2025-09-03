---
title: Strengthen test assertions
description: Write specific, regression-proof test assertions that validate exact
  expected values rather than allowing ambiguous matches. Avoid assertions that could
  pass with incorrect but similar values.
repository: cypress-io/cypress
label: Testing
language: JavaScript
comments_count: 2
repository_stars: 48850
---

Write specific, regression-proof test assertions that validate exact expected values rather than allowing ambiguous matches. Avoid assertions that could pass with incorrect but similar values.

**Problems with weak assertions:**
- `expect(a).eq(b)` passes even if both are `undefined`
- Comparing two dynamic values that could both be wrong
- Missing type validation that could catch unexpected data types

**Better assertion patterns:**

```javascript
// Instead of just comparing two potentially undefined values
expect(Cypress.currentTest.title).eq(cy.state('runnable').ctx.currentTest.title)

// Add type validation and literal value checks
expect(Cypress.currentTest.title)
  .to.be.a('string')
  .eq(cy.state('runnable').title)
  .eq('returns current test runnable properties')
```

**Key improvements:**
1. **Type validation**: Use `.to.be.a('string')` to ensure expected data types
2. **Literal comparisons**: Compare against known string literals when possible
3. **Multiple assertions**: Chain assertions to validate different aspects
4. **Avoid symmetric comparisons**: Don't just compare two dynamic values that could both be wrong

This approach makes tests more reliable by catching edge cases where both compared values might be incorrect in the same way, and provides clearer failure messages when assertions fail.