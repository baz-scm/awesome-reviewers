---
title: proper async error testing
description: When testing for expected errors in async code, use Jest's built-in async
  error testing patterns instead of try-catch blocks with expectations inside catch
  handlers. Expectations in catch blocks can be silently skipped if the code stops
  failing, leading to false positives.
repository: prisma/prisma
label: Testing
language: TypeScript
comments_count: 4
repository_stars: 42967
---

When testing for expected errors in async code, use Jest's built-in async error testing patterns instead of try-catch blocks with expectations inside catch handlers. Expectations in catch blocks can be silently skipped if the code stops failing, leading to false positives.

Use `await expect(promise).rejects.toThrow()` or similar matchers:

```typescript
// ❌ Avoid - expectation can be skipped if error stops occurring
it('should handle error', async () => {
  await ctx.cli('generate').catch((e) => {
    expect(e.stderr).toMatchInlineSnapshot(`Error: ...`)
  })
})

// ✅ Preferred - ensures the promise actually rejects
it('should handle error', async () => {
  const result = ctx.cli('generate')
  await expect(result).rejects.toThrowErrorMatchingInlineSnapshot(`Error: ...`)
})
```

Additionally, ensure your tests actually verify what they claim to test. For example, when testing that an example file was used, assert that the expected content is present, not just that some generic content exists.

For tests that are expected to fail temporarily, use `it.failing()` to make the intent explicit and easier to fix later when the underlying issue is resolved.