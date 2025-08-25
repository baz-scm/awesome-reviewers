---
title: Use modern null handling
description: Leverage modern JavaScript operators and patterns for cleaner, more robust
  null and undefined handling. This improves code readability and reduces boilerplate
  while maintaining safety.
repository: discourse/discourse
label: Null Handling
language: Other
comments_count: 9
repository_stars: 44898
---

Leverage modern JavaScript operators and patterns for cleaner, more robust null and undefined handling. This improves code readability and reduces boilerplate while maintaining safety.

**Key patterns to adopt:**

1. **Nullish coalescing (`??`)** for default values when you specifically want to handle `null` and `undefined`:
```javascript
// Instead of
return this.args.onChange ? this.args.onChange : () => {};
// Use
return this.args.onChange ?? (() => {});
```

2. **Nullish coalescing assignment (`??=`)** for lazy initialization:
```javascript
// Instead of
if (!this.#pendingCleanup[phase]) {
  this.#pendingCleanup[phase] = [];
}
// Use
this.#pendingCleanup[phase] ??= [];
```

3. **Logical OR assignment (`||=`)** for falsy value defaults:
```javascript
// Instead of
value = value || "";
// Use
value ||= "";
```

4. **Leverage truthy/falsy behavior** to simplify boolean checks:
```javascript
// Instead of
return d.hours() !== 0 || d.minutes() !== 0 || d.seconds() !== 0;
// Use
return d.hours() || d.minutes() || d.seconds();

// Instead of
.filter((e) => e)
// Use
.filter(Boolean)
```

5. **Avoid redundant null checks** when functions handle undefined gracefully:
```javascript
// Instead of
if (this.handleBlurTimer) {
  cancel(this.handleBlurTimer);
}
// Use (since cancel handles undefined)
cancel(this.handleBlurTimer);
```

These patterns reduce code verbosity while maintaining or improving null safety, and they clearly express intent about how null/undefined values should be handled.