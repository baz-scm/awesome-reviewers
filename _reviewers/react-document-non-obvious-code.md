---
title: Document non-obvious code
description: 'Always add explanatory comments for code that isn''t immediately clear
  without context. This includes:


  1. Non-standard usage of fields or data structures'
repository: facebook/react
label: Documentation
language: Javascript
comments_count: 2
repository_stars: 236851
---

Always add explanatory comments for code that isn't immediately clear without context. This includes:

1. Non-standard usage of fields or data structures
2. Magic numbers or hardcoded values
3. Clever optimizations or hacks
4. Complex algorithms or transformations

Comments should explain the reasoning behind the approach rather than simply restating what the code does. This helps other developers understand the code more quickly and reduces the likelihood of introducing bugs during future modifications.

Example 1 - When repurposing fields:
```javascript
// We use the reason field to stash the controller since we already have that
// field. It's a bit of a hack but efficient.
return new ReactPromise(RESOLVED_MODEL, value, response);
```

Example 2 - When using magic numbers:
```javascript
// Extract 'Object' from '[object Object]':
return name.slice(8, name.length - 1);
```

## Discussions

## thread:2162366215

@@ -486,31 +472,31 @@ function createResolvedModelChunk<T>(
   value: UninitializedModel,
 ): ResolvedModelChunk<T> {
   // $FlowFixMe[invalid-constructor] Flow doesn't support functions as constructors
-  return new ReactPromise(RESOLVED_MODEL, value, null, response);
+  return new ReactPromise(RESOLVED_MODEL, value, response);

### unstubbable

A comment like we have for `createInitializedStreamChunk` would help avoid confusion:
```
// We use the reason field to stash the controller since we already have that
// field. It's a bit of a hack but efficient.
```

### sebmarkbage

It's all over every access in this file and indeed every Fiber field too. At some point you just got to add a doc for the whole repo.

## thread:2160458343

@@ -80,9 +92,7 @@ export function isSimpleObject(object: any): boolean {
 export function objectName(object: mixed): string {
   // $FlowFixMe[method-unbinding]
   const name = Object.prototype.toString.call(object);
-  return name.replace(/^\[object (.*)\]$/, function (m, p0) {
-    return p0;
-  });
+  return name.slice(8, name.length - 1);

### unstubbable

With the regex now gone, a comment explaining the magic 8 would be nice, e.g.:
```suggestion
  // Extract 'Object' from '[object Object]':
  return name.slice(8, name.length - 1);
```

