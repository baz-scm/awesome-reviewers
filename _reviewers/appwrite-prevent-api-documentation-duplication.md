---
title: Prevent API documentation duplication
description: 'When maintaining API specification files (like OpenAPI or Swagger),
  ensure consistency and avoid duplication that can confuse documentation generators
  and API consumers:'
repository: appwrite/appwrite
label: Documentation
language: Json
comments_count: 2
repository_stars: 51959
---

When maintaining API specification files (like OpenAPI or Swagger), ensure consistency and avoid duplication that can confuse documentation generators and API consumers:

1. **Eliminate duplicate service definitions** - Remove or merge tags that represent the same service with different names (e.g., "projects" and "project").

2. **Standardize naming conventions** - Use consistent casing and plural/singular forms for similar entities across all documentation.

3. **Maintain consistent style** - Ensure all descriptions:
   - End with proper punctuation (typically periods)
   - Use correct grammar
   - Maintain consistent tone and formatting

Example:
```json
// BAD: Duplicate tags with inconsistent descriptions
"tags": [
  {
    "name": "projects",
    "description": "The Project service allows you to manage all the projects in your Appwrite server."
  },
  {
    "name": "project",
    "description": "The Project service allows you to manage all the projects in your Appwrite server."
  }
]

// GOOD: Single, well-defined tag
"tags": [
  {
    "name": "projects",
    "description": "The Projects service allows you to manage all the projects in your Appwrite server."
  }
]
```

This consistency helps maintain clear documentation and prevents confusion in generated code or documentation.