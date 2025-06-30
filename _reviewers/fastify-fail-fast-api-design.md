---
title: Fail-fast API design
description: APIs should be designed to fail fast and explicitly when preconditions
  aren't met, rather than continuing with undefined behavior. This approach makes
  errors immediately visible and prevents subtle, hard-to-debug issues.
repository: fastify/fastify
label: API
language: Markdown
comments_count: 3
repository_stars: 34055
---

APIs should be designed to fail fast and explicitly when preconditions aren't met, rather than continuing with undefined behavior. This approach makes errors immediately visible and prevents subtle, hard-to-debug issues.

When accessing properties or calling methods on your API:

1. Throw explicit, descriptive errors when required resources are missing
2. Validate dependencies at the earliest possible moment
3. Avoid silent failures or undefined behavior

For example, consider these two approaches for handling missing decorators:

```js
// PROBLEMATIC: Silent failure with unclear cause
const user = request.user;
if (user && user.isAdmin) {
  // Execute admin tasks.
}
// If request.user is undefined, it's unclear if:
// - User is unauthenticated, or
// - The 'user' decorator was never declared

// BETTER: Explicit error with clear cause
try {
  const user = request.getDecorator('user');
  if (user.isAdmin) {
    // Execute admin tasks.
  }
} catch (error) {
  // Explicit FST_ERR_DEC_UNDECLARED error is thrown
  // We know precisely that the decorator wasn't declared
}
```

Similarly, when updating values:

```js
// PROBLEMATIC: Silent property assignment without validation
request.user = { name: 'Jean' }; // Works even if 'user' decorator was never declared

// BETTER: Validated assignment with safety checks
// Will throw FST_ERR_DEC_UNDECLARED if 'user' wasn't properly declared
request.setDecorator('user', { name: 'Jean' });
```

This approach applies the principle that declaration and assignment should be distinct operations, similar to how variables work in most programming languages. By enforcing this distinction in your APIs, you create more reliable, self-documenting interfaces that prevent common errors.