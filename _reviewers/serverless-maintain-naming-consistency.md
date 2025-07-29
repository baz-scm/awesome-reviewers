---
title: maintain naming consistency
description: Ensure consistent naming patterns across related components and configurations.
  When naming properties, methods, or identifiers that relate to the same concept,
  use the same form (singular/plural, casing, terminology) throughout the codebase.
repository: serverless/serverless
label: Naming Conventions
language: Markdown
comments_count: 2
repository_stars: 46810
---

Ensure consistent naming patterns across related components and configurations. When naming properties, methods, or identifiers that relate to the same concept, use the same form (singular/plural, casing, terminology) throughout the codebase.

This prevents confusion and maintains predictability for developers working with related features. Inconsistent naming can lead to errors and makes the API harder to learn and use.

Example of inconsistent naming to avoid:
```yaml
# Inconsistent - mixing singular and plural forms
provider:
  websockets:  # plural form
    useProviderTags: true
functions:
  handler:
    events:
      - websocket:  # singular form (event name)
```

Correct approach:
```yaml
# Consistent - using singular form throughout
provider:
  websocket:  # matches the event name
    useProviderTags: true
functions:
  handler:
    events:
      - websocket:  # singular form (event name)
```

Always check that related components use consistent naming conventions, especially when they reference the same underlying concept or feature.