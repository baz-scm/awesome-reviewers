---
title: Deterministic test setup/teardown
description: E2E tests should be deterministic by (1) registering mocks/fixtures before
  any action that triggers network calls (e.g., `goto()`), and (2) handling cleanup
  failures in a way that doesn’t skip subsequent tests/hooks.
repository: maximhq/bifrost
label: Testing
language: TypeScript
comments_count: 2
repository_stars: 6862
---

E2E tests should be deterministic by (1) registering mocks/fixtures before any action that triggers network calls (e.g., `goto()`), and (2) handling cleanup failures in a way that doesn’t skip subsequent tests/hooks.

Apply these rules:
- Register mocks in a `beforeEach` that runs *before* navigation/side effects.
- Track created resources and attempt cleanup in `afterEach`.
- Avoid throwing inside `afterEach` when it can prevent later tests/hooks from running (especially with serial execution). Instead, record leaks and fail in `afterAll`.

Example pattern:
```ts
const created: { provider: string; keyName: string }[] = [];
const leaked: typeof created = [];

test.describe('Some e2e flow', () => {
  test.describe.configure({ mode: 'serial' });

  test.beforeEach(async ({ page }) => {
    // Register mocks BEFORE navigation triggers API calls
    await mockSomeApis(page);
    await providersPage.goto();
  });

  test.afterEach(async ({ providersPage }) => {
    for (const { provider, keyName } of [...created]) {
      try {
        await providersPage.selectProvider(provider);
        const exists = await providersPage.keyExists(keyName, 2000);
        if (exists) await providersPage.deleteKey(keyName);
      } catch (e) {
        leaked.push({ provider, keyName });
      }
    }
    created.length = 0;
  });

  test.afterAll(() => {
    if (leaked.length) {
      throw new Error(`Leaked resources: ${leaked.map(k => `${k.provider}/${k.keyName}`).join(', ')}`);
    }
  });
});
```
This prevents cascading skips, ensures mocks reliably intercept navigation-time calls, and still surfaces real cleanup problems loudly at the end of the suite.