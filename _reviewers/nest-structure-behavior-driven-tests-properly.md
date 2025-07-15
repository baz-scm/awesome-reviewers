---
title: Structure behavior-driven tests properly
description: Organize tests using behavior-driven development (BDD) patterns to improve
  clarity and maintainability. Group related tests using descriptive `describe` blocks
  for methods/scenarios, and write clear test cases that focus on testing behavior
  rather than implementation details.
repository: nestjs/nest
label: Testing
language: TypeScript
comments_count: 6
repository_stars: 71766
---

Organize tests using behavior-driven development (BDD) patterns to improve clarity and maintainability. Group related tests using descriptive `describe` blocks for methods/scenarios, and write clear test cases that focus on testing behavior rather than implementation details.

Key principles:
1. Use nested describe blocks to group related tests
2. Write descriptive test cases that explain the expected behavior
3. Test public interfaces instead of implementation details
4. Avoid redundant test calls
5. Focus assertions on behavior verification

Example:
```typescript
describe('CatsService', () => {
  describe('findAll', () => {
    it('should return an array of cats', async () => {
      // Test the actual service behavior, don't mock what you're testing
      const result = await catsService.findAll();
      await expect(result).resolves.toEqual(expectedCats);
    });
  });

  describe('create', () => {
    describe('when provided valid cat data', () => {
      it('should successfully create a new cat', async () => {
        const newCat = { name: 'Whiskers', age: 2 };
        const result = await catsService.create(newCat);
        expect(result).toMatchObject(newCat);
      });
    });
  });
});
```