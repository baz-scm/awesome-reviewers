---
title: Document configuration requirements
description: Ensure that configuration requirements, dependencies, and options are
  clearly documented and communicated to users. When introducing features that require
  external configuration or have configurable behavior, explicitly state what must
  be configured and provide clear guidance on the implications of different settings.
repository: better-auth/better-auth
label: Configurations
language: Other
comments_count: 2
repository_stars: 19651
---

Ensure that configuration requirements, dependencies, and options are clearly documented and communicated to users. When introducing features that require external configuration or have configurable behavior, explicitly state what must be configured and provide clear guidance on the implications of different settings.

For configuration dependencies, use strong emphasis to highlight mandatory requirements:

```markdown
This is an advanced feature. Configuration outside of this plugin **MUST** be provided.
```

For configuration options, clearly explain the conditions and effects:

```markdown
If you want your users to link a social account with a different email address than their existing one, you'll need to enable this in the account linking settings.
```

This practice prevents configuration-related issues, reduces support burden, and helps developers understand the full scope of setup requirements for features they implement.