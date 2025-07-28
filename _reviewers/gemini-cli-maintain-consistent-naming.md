---
title: Maintain consistent naming
description: Ensure naming consistency across all contexts where an identifier appears
  - configuration files, code enums, documentation, and user interfaces. Names should
  be semantically clear and distinguish between related but different entities.
repository: google-gemini/gemini-cli
label: Naming Conventions
language: Markdown
comments_count: 3
repository_stars: 65062
---

Ensure naming consistency across all contexts where an identifier appears - configuration files, code enums, documentation, and user interfaces. Names should be semantically clear and distinguish between related but different entities.

When the same concept appears in multiple places, use identical naming:
- Configuration keys should match their corresponding code constants
- Documentation examples should reflect actual implementation names
- User-facing strings should align with internal representations

Prefer simple, unambiguous names that avoid unnecessary complexity:

```json
// Good: Consistent across config and code
"selectedAuthType": "oauth" // matches AuthType.OAUTH in code

// Bad: Inconsistent naming
"selectedAuthType": "oauth-personal" // while code uses AuthType.LOGIN_WITH_GOOGLE
```

For related but distinct entities, use clear semantic distinctions:
- "Claude" (the LLM) vs "Claude Code" (the application)
- "gemini" (API service) vs "gemini-api" (authentication method)

When naming conflicts arise, implement graceful resolution strategies that preserve the original simple names for the most common cases while providing clear alternatives for conflicts.