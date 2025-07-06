---
title: Use guards over assertions
description: Prefer explicit type guards and null checks over TypeScript's type assertions
  (`as`) when handling potentially null or undefined values. Type assertions bypass
  TypeScript's type checking system and can lead to runtime errors.
repository: apache/airflow
label: Null Handling
language: TSX
comments_count: 2
repository_stars: 40858
---

Prefer explicit type guards and null checks over TypeScript's type assertions (`as`) when handling potentially null or undefined values. Type assertions bypass TypeScript's type checking system and can lead to runtime errors.

Instead:
1. Use nullish coalescing operator (`??`) to provide default values
2. Implement explicit type guards with `Array.isArray()` and property checks
3. Use type predicates for more complex validations

Example (Before):
```typescript
const menuPlugins = (useConfig("plugins_extra_menu_items") as Array<ExternalViewResponse>) ?? [];
```

Example (After):
```typescript
const menuItems = useConfig("plugins_extra_menu_items");
const menuPlugins = Array.isArray(menuItems) ? menuItems : [];

// Or with additional type validation:
if (
  Array.isArray(menuItems) &&
  menuItems.every(item => "name" in item && "href" in item)
) {
  // Safe to use menuItems here
}
```

This approach ensures runtime safety beyond compile-time type checking and reduces the risk of unexpected null reference exceptions.