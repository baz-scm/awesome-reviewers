---
title: Behavioral Testing Standards
description: When adding or modifying tests, aim for **behavioral, user-facing coverage**
  that uses **public observables** and **standard test utilities**, and avoid coupling
  to React/implementation internals.
repository: facebook/react#b16
label: Testing
language: JavaScript
comments_count: 9
repository_stars: 251891
---

When adding or modifying tests, aim for **behavioral, user-facing coverage** that uses **public observables** and **standard test utilities**, and avoid coupling to React/implementation internals.

**Do:**
- Reproduce the scenario the way React/users experience it (e.g., interact with the DOM/React root inside `act`, rather than manually simulating internal operation orders).
- Assert on outcomes/logs that represent what the system exposes (DOM visibility, rendered output, Scheduler events), not on internal mechanics.
- Prefer repo-standard helpers (e.g., `Scheduler.log`/`assertLog`, `waitForMicrotasks`, `assertConsoleErrorDev`, `spyOn` + `restoreAllMocks`).
- Keep assertions explicit and scan-friendly: take fresh references/instances for each assertion and verify state before/after transitions.

**Don’t:**
- Test by reordering internal constants/operation streams unless that *is* the public contract.
- Encode brittle “React implementation detail” expectations in comments or hidden assumptions.
- Mock/intercept module internals as a first resort; assert against public behavior instead.

**Example (move user action into an `act` scope + assert via Scheduler logs):**
```js
import {act} from 'internal-test-utils';

it('multiple rapid submissions do not throw', async () => {
  const submitBtn = document.createElement('button');
  const form = document.createElement('form');
  submitBtn.textContent = 'Submit';
  form.appendChild(submitBtn);

  // Arrange your UI so clicks trigger the real submit path.
  // (Avoid implementing the double-submit inside the component itself.)

  Scheduler.log('Render');

  await act(async () => {
    // first click
    submitBtn.click();
    await waitFor(['Render']);

    // second click immediately after
    submitBtn.click();
    await waitFor(['Render']);
  });
});
```

Adopting this standard will reduce test brittleness, increase confidence that changes won’t break real user flows, and keep tests consistent with existing patterns across the codebase.