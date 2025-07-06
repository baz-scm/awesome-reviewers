---
title: Use direct documentation style
description: 'Write documentation using direct, clear language that addresses the
  reader directly. Follow these style guidelines:


  1. Use direct address instead of referring to "users" - write "You can configure..."
  rather than "Users can configure..."'
repository: astral-sh/uv
label: Documentation
language: Markdown
comments_count: 4
repository_stars: 60322
---

Write documentation using direct, clear language that addresses the reader directly. Follow these style guidelines:

1. Use direct address instead of referring to "users" - write "You can configure..." rather than "Users can configure..."

2. Avoid words like "simply" that minimize complexity - recognize that what seems simple to documentation authors may not be obvious to all readers.

3. Maintain consistent formatting for technical elements (HTTP status codes, command options, etc.) throughout documentation.

4. Keep guides focused on common workflows with appropriate detail levels, saving complex explanations for reference documentation.

Example - Instead of:
```
When using the `first-index` strategy, uv will stop searching if it encounters a `401 Unauthorized` 
or `403 Forbidden` response status code. Users can configure which error codes are ignored for an 
index, using the `ignored-error-codes` setting.
```

Write:
```
When using the first-index strategy, uv will stop searching if an HTTP 401 Unauthorized 
or HTTP 403 Forbidden status code is encountered. To ignore additional error codes for an index, 
use the `ignored-error-codes` setting.
```

This style creates documentation that feels more approachable while maintaining technical accuracy.