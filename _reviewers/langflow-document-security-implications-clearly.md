---
title: Document security implications clearly
description: When documenting features that involve sensitive data, authentication,
  or privileged operations, explicitly state the security implications and use appropriate
  warning levels to ensure users understand potential risks.
repository: langflow-ai/langflow
label: Security
language: Markdown
comments_count: 3
repository_stars: 111046
---

When documenting features that involve sensitive data, authentication, or privileged operations, explicitly state the security implications and use appropriate warning levels to ensure users understand potential risks.

This includes:
- Using `:::warning` instead of `:::important` when documenting features that could expose sensitive information like API keys
- Clearly explaining the scope and privileges associated with API keys, especially for superuser accounts
- Including security considerations for file handling, such as data retention, access controls, and deletion procedures
- Providing guidance on protecting sensitive data when using features like file uploads or flow exports

Example from API key documentation:
```markdown
:::warning
An API key represents the user who created it. If you create a key as a superuser, then that key will have superuser privileges.
Anyone who has that key can authorize superuser actions through the Langflow API, including user management and flow management.
:::
```

This practice helps users make informed security decisions and prevents inadvertent exposure of sensitive information through better awareness of security implications.