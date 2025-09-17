---
title: API payload structure
description: Design API request and response payloads to match their specific purpose
  rather than forcing them to conform to existing application types. When API payloads
  require different structures or optional fields compared to internal data models,
  create dedicated API-specific types instead of adding placeholder values or compromising
  type safety.
repository: langgenius/dify
label: API
language: TypeScript
comments_count: 2
repository_stars: 114231
---

Design API request and response payloads to match their specific purpose rather than forcing them to conform to existing application types. When API payloads require different structures or optional fields compared to internal data models, create dedicated API-specific types instead of adding placeholder values or compromising type safety.

This prevents situations where developers must add dummy values like empty strings to satisfy type requirements that don't align with the API's actual needs. It also enables cleaner API interfaces with appropriate optional parameters and nested data structures.

Example of the problem:
```typescript
// Problematic: Forcing API payload to match internal type
environment_variables: environmentVariables.map((item: EnvironmentVariable) => {
  return {
    id: item.id,
    name: item.name,
    value_type: item.value_type,
    from_version: restoredSecretsInfo[item.id].from_version,
    // Adding dummy values to satisfy EnvironmentVariable type
    value: '',
    description: '',
  }
})
```

Better approach: Create API-specific types that reflect the actual payload structure and requirements, allowing for cleaner, more maintainable interfaces that don't require workarounds or placeholder data.