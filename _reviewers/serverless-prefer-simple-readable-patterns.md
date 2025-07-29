---
title: prefer simple readable patterns
description: Choose simple, readable code patterns over complex alternatives. Avoid
  unnecessary complexity that doesn't add functional value but makes code harder to
  understand and maintain.
repository: serverless/serverless
label: Code Style
language: JavaScript
comments_count: 8
repository_stars: 46810
---

Choose simple, readable code patterns over complex alternatives. Avoid unnecessary complexity that doesn't add functional value but makes code harder to understand and maintain.

Key principles:
- Use async/await instead of Promise chains for better readability
- Choose appropriate array methods (use `some()` for boolean checks, not `find()`)
- Avoid overusing `reduce()` when simple iteration is clearer
- Remove commented code and eslint-disable comments
- Return directly instead of wrapping in `Promise.resolve()`
- Avoid stylistic changes that don't improve functionality

Examples:

```javascript
// Prefer this (simple async/await)
try {
  await fs.promises.access(join(workingDir, input));
  return `Path ${input} is already taken`;
} catch {
  return true;
}

// Over this (Promise chains)
fs.promises.access(join(workingDir, input))
  .then(() => `Path ${input} is already taken`)
  .catch(() => true)

// Prefer this (appropriate method choice)
if (!Object.keys(resources).some(key => 
  resources[key].Type === 'AWS::Lambda::LayerVersion'
)) {
  // handle case
}

// Over this (wrong method for boolean check)
if (!Object.keys(resources).find(key => 
  resources[key].Type === 'AWS::Lambda::LayerVersion'
)) {
  // handle case
}

// Prefer this (simple iteration)
const result = [];
for (const param of params) result.push(...param);
return { value: result };

// Over this (unnecessary reduce complexity)
return params.reduce((acc, item) => {
  acc.push(...item);
  return acc;
}, []);
```

This approach improves code maintainability, reduces cognitive load, and makes the codebase more accessible to all team members.