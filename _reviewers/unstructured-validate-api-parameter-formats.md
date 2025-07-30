---
title: Validate API parameter formats
description: Ensure API parameters match the expected format and structure of target
  APIs before runtime. Validate parameter types, required fields, and data structures
  during development rather than discovering mismatches through runtime errors.
repository: Unstructured-IO/unstructured
label: API
language: Shell
comments_count: 2
repository_stars: 12117
---

Ensure API parameters match the expected format and structure of target APIs before runtime. Validate parameter types, required fields, and data structures during development rather than discovering mismatches through runtime errors.

When integrating with external APIs, explicitly validate that:
- Parameter formats match API specifications (e.g., single values vs arrays)
- Authentication methods are clearly defined through parameters rather than implicit environment setup
- Required fields and data structures are properly formatted

Example of problematic parameter passing:
```bash
# Incorrect - API expects array but single value provided
--requested-indexing-policy '{"deny": "metadata"}'

# Correct - API expects array format
--requested-indexing-policy '{"deny": ["metadata"]}'
```

Additionally, make authentication explicit through parameters:
```bash
# Better - explicit parameter
--embedding-api-key "$VERTEX_API_KEY"

# Rather than relying on implicit environment variables
# GOOGLE_APPLICATION_CREDENTIALS (less obvious to users)
```

This prevents runtime failures and makes API integrations more maintainable and user-friendly.