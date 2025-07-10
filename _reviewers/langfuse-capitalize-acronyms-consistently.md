---
title: Capitalize acronyms consistently
description: Use standard capitalization for acronyms in all identifiers, method names,
  variables, and other code elements. Common acronyms like 'API', 'URL', 'JSON', 'HTML',
  and 'XML' should be written in all uppercase letters.
repository: langfuse/langfuse
label: Naming Conventions
language: Json
comments_count: 2
repository_stars: 13574
---

Use standard capitalization for acronyms in all identifiers, method names, variables, and other code elements. Common acronyms like 'API', 'URL', 'JSON', 'HTML', and 'XML' should be written in all uppercase letters.

This applies to all contexts:
- Function names: `getAPIKeys` instead of `getApiKeys`
- Variable names: `userAPIConfig` instead of `userApiConfig`
- API endpoint names: `"name": "Get API Keys"` instead of `"name": "Get Api Keys"`
- Text content in comments and documentation

For example, in our API endpoint definitions:

```json
{
  "_type": "endpoint",
  "name": "Get API Keys",  // Correct - acronym fully capitalized
  ...
}
```

Instead of:

```json
{
  "_type": "endpoint",
  "name": "Get Api Keys",  // Incorrect - inconsistent acronym capitalization
  ...
}
```

Consistent acronym capitalization improves code readability, maintains professional standards across the codebase, and helps ensure interface consistency for users.