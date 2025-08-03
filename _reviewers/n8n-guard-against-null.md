---
title: Guard against null
description: Always use optional chaining (`?.`) and nullish coalescing (`??`) operators
  when accessing potentially undefined or null properties. These patterns prevent
  TypeErrors when accessing nested properties and provide appropriate defaults only
  when values are null or undefined.
repository: n8n-io/n8n
label: Null Handling
language: TypeScript
comments_count: 14
repository_stars: 122978
---

Always use optional chaining (`?.`) and nullish coalescing (`??`) operators when accessing potentially undefined or null properties. These patterns prevent TypeErrors when accessing nested properties and provide appropriate defaults only when values are null or undefined.

```typescript
// Unsafe - may throw TypeError:
const message = runData.data[NodeConnectionTypes.Main][0][0].evaluationData;
const activeModules = [...settings.value.activeModules, 'data-store'];
const isMFAEnforced = settings.value.enterprise.mfaEnforcement;

// Safe - uses proper null handling:
const message = runData?.data?.[NodeConnectionTypes.Main]?.[0]?.[0]?.evaluationData ?? {};
const activeModules = [...(settings.value.activeModules ?? []), 'data-store'];
const isMFAEnforced = settings.value.enterprise?.mfaEnforcement ?? false;
```

When handling arrays from potentially empty sources, provide empty array defaults and filter out falsy values:

```typescript
// Handle empty split results with proper filtering
const selectedApps = currentUserCloudInfo.value?.selectedApps?.split(',').filter(Boolean) ?? [];

// Check object existence before property access
if (toolOrToolkit && typeof (toolOrToolkit as Toolkit).getTools === 'function') {
  // Now safe to call the method
}

// Use proper object access patterns to avoid null reference errors
const hasNodeRun = Object.prototype.hasOwnProperty.call(runData ?? {}, node.name);
```

Always ensure your type definitions accurately represent nullable values. If an API can return `null` for a field, include it in the type:

```typescript
// Accurate type for a field that can be null
interface Response {
  stop_reason: string | null;
}
```