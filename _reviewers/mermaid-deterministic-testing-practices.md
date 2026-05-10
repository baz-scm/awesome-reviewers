---
title: Deterministic Testing Practices
description: 'Integration/e2e tests should be deterministic and directly tied to specified
  behavior.


  Apply these rules:

  1) Avoid time-based waits. Wait for an observable condition (DOM element present,
  network idle, event emitted, SVG rendered) instead of `cy.wait(500)`.'
repository: mermaid-js/mermaid
label: Testing
language: JavaScript
comments_count: 6
repository_stars: 87952
---

Integration/e2e tests should be deterministic and directly tied to specified behavior.

Apply these rules:
1) Avoid time-based waits. Wait for an observable condition (DOM element present, network idle, event emitted, SVG rendered) instead of `cy.wait(500)`.
2) Make syntax/format expectations strict. When behavior depends on parsing (e.g., `dateRange`), define the accepted format precisely and test the exact edge cases (whitespace/colon/spacing variants, valid date-only/time-only/date+time cases).
3) Eliminate flakiness from external assets. For font/icon rendering, use a stable local asset source and/or wait for fonts to finish loading before rendering/asserting.
4) Keep snapshot identifiers stable. If your visual tests compare images, avoid changing snapshot keys/titles; add tests within existing `describe` blocks to prevent snapshot mismatch.

Example (replace time-based waits):
```js
// Bad (flaky)
cy.wait(500);

// Prefer (event/condition-based)
cy.get('svg', { timeout: 10_000 }).should('exist');
// or: wait for a specific rendered marker / data attribute
// cy.get('[data-testid="render-complete"]', { timeout: 10_000 }).should('be.visible');
```

Example (strict format tests for parsing):
```js
const ok = 'dateRange : 13:00, 14:00';
const bad1 = 'dateRange: 13:00, 14:00';
const bad2 = 'dateRange 13:00, 14:00';

expect(parserFnConstructor(`gantt\n${ok}`)).not.toThrow();
expect(parserFnConstructor(`gantt\n${bad1}`)).toThrow();
expect(parserFnConstructor(`gantt\n${bad2}`)).toThrow();
```