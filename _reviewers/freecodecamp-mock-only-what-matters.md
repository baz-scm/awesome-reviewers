---
title: Mock Only What Matters
description: 'When writing tests, avoid introducing unnecessary fakes/mocks that hide
  real integration behavior.


  - If your goal is to validate how code interacts with DOM dependencies, don’t “fake”
  core event/data shapes more than needed; use the real DOM/events interface (or a
  higher-fidelity fixture) so failures reflect real breakage.'
repository: freeCodeCamp/freeCodeCamp
label: Testing
language: TSX
comments_count: 2
repository_stars: 444449
---

When writing tests, avoid introducing unnecessary fakes/mocks that hide real integration behavior.

- If your goal is to validate how code interacts with DOM dependencies, don’t “fake” core event/data shapes more than needed; use the real DOM/events interface (or a higher-fidelity fixture) so failures reflect real breakage.
- Keep mocking minimal and scoped to the unit under test: hoist/stabilize only what must be shared or stable, and define the rest inline to prevent extra complexity and to reduce coupling to singleton/module state.

Example (minimal mocking in a hook test):

```ts
import { renderHook } from '@testing-library/react';
import { vi } from 'vitest';

const { mockDispatch } = vi.hoisted(() => ({
  mockDispatch: vi.fn(),
}));

// inline mock for the second dependency to keep the hook isolated and readable
vi.mock('./some-module', () => ({
  useSingleton: () => ({
    dispatch: mockDispatch,
    initialize: vi.fn(),
  }),
}));

// renderHook(...) 
```

Practical checklist:
- What behavior is the test asserting?
- Does the setup replace real interfaces with unrealistic fakes?
- Are there mocks/fixtures that aren’t required for the assertion? Remove or inline them.
- If a dependency changes (DOM structure/events/interaction contract), will this test fail in a meaningful way?