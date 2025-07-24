---
title: Match defaults to types
description: When specifying default values in schemas or configurations, ensure they
  match the declared type to prevent validation errors and unpredictable behavior.
  For object types, use empty objects (`{}`) not null, undefined, or arrays. For string
  types that should be empty by default, use empty strings (`""`) not null. This practice
  improves type safety and...
repository: appwrite/appwrite
label: Null Handling
language: Json
comments_count: 2
repository_stars: 51959
---

When specifying default values in schemas or configurations, ensure they match the declared type to prevent validation errors and unpredictable behavior. For object types, use empty objects (`{}`) not null, undefined, or arrays. For string types that should be empty by default, use empty strings (`""`) not null. This practice improves type safety and prevents runtime type errors.

```diff
// INCORRECT: Type mismatch between declared type and default
{
  "type": "object",
  "description": "Document data as JSON object.",
  "default": [],  // An array default for an object type
}

// CORRECT: Type-consistent defaults
{
  "type": "object",
  "description": "Document data as JSON object.",
  "default": {},  // An object default for an object type
}

// CORRECT: Empty string default for optional string
{
  "type": "string",
  "description": "Optional document ID",
  "default": "",  // Empty string instead of null
}
```