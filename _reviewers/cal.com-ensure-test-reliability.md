---
title: ensure test reliability
description: Write tests that are stable, independent, and non-flaky by following
  proper isolation and waiting practices. Tests should create their own data, clean
  up after themselves, and avoid dependencies on other tests or external state.
repository: calcom/cal.com
label: Testing
language: TypeScript
comments_count: 5
repository_stars: 37732
---

Write tests that are stable, independent, and non-flaky by following proper isolation and waiting practices. Tests should create their own data, clean up after themselves, and avoid dependencies on other tests or external state.

Key practices:
- **Test Isolation**: Each test should create its own test data and clean up afterward to avoid dependencies between tests
- **Proper Waiting**: Use `waitForLoadState("networkidle")` or wait for specific elements instead of arbitrary timeouts with `waitForTimeout()`
- **Avoid Hardcoded Values**: Use dynamic values (like `randomString()`) instead of hardcoded identifiers that might conflict
- **Cleanup Resources**: Always clean up created test data to prevent state leakage

Example of proper test isolation:
```typescript
it("should create the membership of the org", async () => {
  // Create test user for this specific test
  const testUserForCreate = await userRepositoryFixture.create({
    email: `test-create-${randomString()}@api.com`,
    username: `test-create-${randomString()}`,
  });

  return request(app.getHttpServer())
    .post(`/v2/organizations/${org.id}/memberships`)
    .send({ userId: testUserForCreate.id, accepted: true, role: "MEMBER" })
    .expect(201)
    .then(async (response) => {
      const createdMembership = response.body.data;
      // ... assertions ...
      
      // Clean up
      await membershipRepositoryFixture.delete(createdMembership.id);
      await userRepositoryFixture.deleteByEmail(testUserForCreate.email);
    });
});
```

Reliable tests reduce CI failures, improve developer confidence, and prevent blocking of development workflows.