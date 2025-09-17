---
title: prefer type guards
description: Use semantic type guards like `isDefined()` instead of basic type checks
  (`typeof`, simple null checks) or unsafe type assertions (`as!`, `!`). Type guards
  provide better readability, type safety, and null reference prevention.
repository: twentyhq/twenty
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 35477
---

Use semantic type guards like `isDefined()` instead of basic type checks (`typeof`, simple null checks) or unsafe type assertions (`as!`, `!`). Type guards provide better readability, type safety, and null reference prevention.

**Prefer this:**
```ts
// Use semantic type guards
if (!isDefined(activeTabId)) return;
if (!isDefined(pageLayout)) {
  throw new PageLayoutException(/*...*/);
}

// Filter out null values
return objectNameSingulars
  .map(name => objectMetadataItems.find(item => item.nameSingular === name))
  .filter(isDefined);
```

**Instead of:**
```ts
// Avoid basic type checks and unsafe assertions
if (!activeTabId) return;  // unclear intent
if (typeof parsed === 'object') { /*...*/ }  // prefer specific type guards
return restoredPageLayout!;  // unsafe assertion
filteredFields[key] = { /*...*/ } as FieldOutputSchemaV2;  // forced typing
```

This approach eliminates null reference errors, makes code intent clearer, and leverages TypeScript's type system for better compile-time safety.