---
title: Validate object availability
description: Always verify that objects and their properties exist before accessing
  them to prevent null reference errors. This includes checking for undefined global
  objects, optional parameters, and nested properties.
repository: block/goose
label: Null Handling
language: TSX
comments_count: 2
repository_stars: 19037
---

Always verify that objects and their properties exist before accessing them to prevent null reference errors. This includes checking for undefined global objects, optional parameters, and nested properties.

When you know an object or property is guaranteed to exist (like when checking `param.default` exists), keep the logic simple and avoid unnecessary validation:

```typescript
// Good: Simple check when we know default exists
if (param.requirement === 'optional' && param.default) {
  initialValues[param.key] = param.default;
}
```

When accessing potentially undefined objects, add explicit checks:

```typescript
// Good: Check object existence before use
useEffect(() => {
  if (window.electron) {
    const currentVersion = window.electron.getVersion();
    setUpdateInfo((prev) => ({ ...prev, currentVersion }));
  }
}, []);
```

This prevents runtime errors and makes your code more robust by handling null/undefined cases explicitly rather than assuming objects will always be available.