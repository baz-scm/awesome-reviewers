---
title: Consistent null safety patterns
description: Apply null safety operators consistently throughout your code to prevent
  runtime errors and improve readability. Use the nullish coalescing operator (??)
  for default values, optional chaining (?.) for safe property access, and simplify
  null checks when semantically equivalent.
repository: discourse/discourse
label: Null Handling
language: JavaScript
comments_count: 4
repository_stars: 44898
---

Apply null safety operators consistently throughout your code to prevent runtime errors and improve readability. Use the nullish coalescing operator (??) for default values, optional chaining (?.) for safe property access, and simplify null checks when semantically equivalent.

Key patterns to follow:
- Use `??` for default values: `const crossAxis = options.crossAxisShift ?? true;` instead of verbose if-statements
- Use `?.` for safe navigation: `topic?.tags || params?.tags` and `topic?.get?.("isPrivateMessage")` 
- Simplify falsy checks when appropriate: `!userFields[siteField.id]` instead of `isEmpty(userFields[siteField.id])` when null/false are equivalent
- Apply these patterns consistently - if you use safe navigation in one place, consider if other similar accesses need it too

This prevents null reference exceptions while keeping code concise and readable. Be mindful that different null safety patterns serve different purposes - choose the right tool for each situation.