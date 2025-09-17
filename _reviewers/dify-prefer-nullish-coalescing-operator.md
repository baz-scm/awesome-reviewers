---
title: prefer nullish coalescing operator
description: Use the nullish coalescing operator (`??`) instead of logical OR (`||`)
  when you want to provide default values only for null or undefined, while preserving
  other falsy values like empty arrays, empty strings, or zero.
repository: langgenius/dify
label: Null Handling
language: TSX
comments_count: 2
repository_stars: 114231
---

Use the nullish coalescing operator (`??`) instead of logical OR (`||`) when you want to provide default values only for null or undefined, while preserving other falsy values like empty arrays, empty strings, or zero.

The `||` operator treats all falsy values (null, undefined, false, 0, "", []) as requiring the default, while `??` only treats null and undefined as requiring the default. This distinction is crucial for preserving intentionally falsy but valid values.

Example:
```typescript
// ❌ Problematic - loses empty arrays
...(draft.file?.allowed_file_types || [])

// ✅ Better - preserves empty arrays  
...(draft.file?.allowed_file_types ?? [])

// ❌ Problematic - loses falsy but valid values
const config = userConfig || defaultConfig

// ✅ Better - only defaults for null/undefined
const config = userConfig ?? defaultConfig
```

This pattern is especially important when working with arrays, objects, or other values where falsy states have semantic meaning that should be preserved.