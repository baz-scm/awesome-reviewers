---
title: Precise Scenario-Based Testing
description: When writing tests, ensure they (1) match the scenario name and input
  data, (2) exercise behavior through the appropriate layer (prefer public/high-level
  APIs so defaults/precedence are covered), (3) use the project’s DOM test helpers/fixtures
  and avoid unnecessary mocks/polyfills, and (4) assert specific outcomes (including
  exact error messages) rather...
repository: mermaid-js/mermaid
label: Testing
language: TypeScript
comments_count: 10
repository_stars: 87952
---

When writing tests, ensure they (1) match the scenario name and input data, (2) exercise behavior through the appropriate layer (prefer public/high-level APIs so defaults/precedence are covered), (3) use the project’s DOM test helpers/fixtures and avoid unnecessary mocks/polyfills, and (4) assert specific outcomes (including exact error messages) rather than broad behaviors.

Apply it like this:
- **Scenario alignment:** Don’t reuse the same input across multiple cases if each test’s name implies different behavior (short/medium/long, enabled/disabled, etc.).
- **Right layer:** If a behavior depends on configuration precedence/defaulting, validate through the same API path production uses (e.g., config APIs), not by indirectly testing internal functions unless there’s no public entrypoint.
- **Mock minimization:** Keep only mocks that the environment truly can’t support; if `jsdomIt` can provide a real DOM, prefer it over spies/mocked D3/cytoscape.
- **Specific assertions:**
  - For failures, assert the **actual error message**.
  - For object identity tests, also assert meaningful fields/types/values when relevant.
- **Maintainability:** Prefer inline snapshots and simpler setup; remove redundant initialization calls when the test doesn’t require them.

Example (DOM test with fixture + specific assertions):
```ts
import { expect } from 'vitest';
import { jsdomIt } from '../test-utils/jsdomIt';
import { select } from 'd3-selection';
import { addSVGa11yTitleDescription } from './a11y';

jsdomIt('does not insert title tag', ({ svg }) => {
  const svgSelection = select<SVGSVGElement, never>(svg);

  addSVGa11yTitleDescription(svgSelection, 'chart-title', undefined, 'givenId');

  const titleNode = svg.querySelector('title');
  expect(titleNode).toBeNull();
});
```

Example (error message assertion):
```ts
await expect(renderSomething(badInput)).rejects.toThrow(
  'Expected exact error message here'
);
```

This combination prevents “false green” tests, improves coverage, reduces brittle mocks, and makes regressions easier to diagnose.