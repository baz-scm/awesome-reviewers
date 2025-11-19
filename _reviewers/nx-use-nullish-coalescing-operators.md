---
title: Use nullish coalescing operators
description: Prefer modern JavaScript nullish coalescing (`??`) and optional chaining
  (`?.`) operators over verbose conditional logic for handling null and undefined
  values. These operators provide cleaner, more readable code while maintaining null
  safety.
repository: nrwl/nx
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 27518
---

Prefer modern JavaScript nullish coalescing (`??`) and optional chaining (`?.`) operators over verbose conditional logic for handling null and undefined values. These operators provide cleaner, more readable code while maintaining null safety.

Use nullish coalescing to provide fallback values:
```typescript
// Instead of complex conditional logic
let newVersion: string;
if (targetVersionData.newVersion === null) {
  newVersion = this.releaseGraph.cachedCurrentVersions.get(dep.target) || currentDependencyVersion;
} else {
  newVersion = targetVersionData.newVersion || currentDependencyVersion;
}

// Use nullish coalescing
const newVersion = 
  targetVersionData.newVersion ?? 
  this.releaseGraph.cachedCurrentVersions.get(dep.target) ?? 
  currentDependencyVersion;
```

Use optional chaining for safe property access:
```typescript
// Safe property access
projectVersionData?.newVersion

// Ensure operators stay together (not split across lines)
delete rootVersionWithoutGlobalOptions.generatorOptions?.someProperty;
```

Add defensive checks even when values "shouldn't" be null, and verify types before operations when parameters can be multiple types:
```typescript
// Protect against unexpected nulls
const preId = prerelease(version)?.[0];
if (typeof preId === 'string') {
  return preId;
}

// Type check before processing
function concurrency(str: string | number) {
  const parallel = typeof str === 'number' ? str : parseInt(str);
}
```