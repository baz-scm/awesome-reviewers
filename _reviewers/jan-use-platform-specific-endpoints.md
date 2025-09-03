---
title: Use platform-specific endpoints
description: When configuring API integrations, always use the actual platform-specific
  endpoints and identifiers rather than generic placeholders. Generic configurations
  often lead to integration failures and confusion for users following documentation.
repository: menloresearch/jan
label: API
language: Other
comments_count: 2
repository_stars: 37620
---

When configuring API integrations, always use the actual platform-specific endpoints and identifiers rather than generic placeholders. Generic configurations often lead to integration failures and confusion for users following documentation.

Ensure that:
- API endpoints point to the correct service-specific URLs
- Model IDs match the exact identifiers used by the target platform
- Configuration examples reflect real, working values

For example, when integrating with Groq API:

```json
{
  "full_url": "https://api.groq.com/openai/v1/chat/completions",
  "api_key": "<your-groq-api-key>"
}
```

And use actual model IDs from the platform:

```json
{
  "id": "mixtral-8x7b-32768",
  // not generic "groq"
}
```

This practice prevents integration failures and ensures documentation accurately reflects working configurations that users can directly implement.