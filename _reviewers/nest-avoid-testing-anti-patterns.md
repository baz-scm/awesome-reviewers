---
title: Avoid testing anti-patterns
description: 'Ensure your tests actually validate functionality by avoiding common
  testing anti-patterns:


  1. **Don''t mock what you''re testing** - When testing a method, don''t mock its
  implementation as this tests nothing meaningful:'
repository: nestjs/nest
label: Testing
language: TypeScript
comments_count: 5
repository_stars: 71767
---

Ensure your tests actually validate functionality by avoiding common testing anti-patterns:

1. **Don't mock what you're testing** - When testing a method, don't mock its implementation as this tests nothing meaningful:

```typescript
// WRONG - mocking the method under test
it('should find all cats', async () => {
  jest.spyOn(catsService, 'findAll').mockImplementation(() => result);
  expect(await catsService.findAll()).toEqual(result);
});

// RIGHT - setting up the state to test the actual implementation
it('should find all cats', async () => {
  // @ts-ignore - access internal state for test setup
  catsService.cats = result;
  expect(await catsService.findAll()).toEqual(result);
});
```

2. **Test public interfaces, not private functions** - Private methods should be tested through public methods. If a private method is complex, consider extracting it to a separate class:

```typescript
// WRONG - testing private methods directly
describe('getPaths', () => { // private method
  it('should return paths', () => {
    expect(middlewareModule['getPaths'](routes)).toEqual(['path1', 'path2']);
  });
});

// RIGHT - test via public interface or extract to a testable class
describe('register', () => { // public method
  it('should configure paths correctly', () => {
    middlewareModule.register(routes);
    // assert the expected behavior
  });
});
```

3. **Don't make redundant test calls** - Call the method once and make all assertions on that single call:

```typescript
// WRONG - calling the method multiple times
it('should create a user', () => {
  usersController.create(createUserDto); // unnecessary call
  expect(usersController.create(createUserDto)).resolves.toEqual({
    id: 'a id',
    ...createUserDto,
  });
});

// RIGHT - single call with multiple assertions
it('should create a user', () => {
  expect(usersController.create(createUserDto)).resolves.toEqual({
    id: 'a id',
    ...createUserDto,
  });
  expect(usersService.create).toHaveBeenCalledWith(createUserDto);
});
```

4. **Test the actual behavior** - Ensure your tests verify functionality, not just that methods were called:

```typescript
// WRONG - only checking if a method was called
it('should remove a user', async () => {
  const removeUserSpy = jest.spyOn(service, 'remove');
  service.remove('anyid');
  expect(removeUserSpy).toHaveBeenCalledWith('anyid');
});

// RIGHT - checking the actual behavior
it('should remove a user', async () => {
  const repositorySpy = jest.spyOn(repository, 'delete');
  await service.remove('anyid');
  expect(repositorySpy).toHaveBeenCalledWith('anyid');
  // and possibly check that the user is actually gone
});