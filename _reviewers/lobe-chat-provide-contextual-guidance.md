---
title: Provide contextual guidance
description: Documentation should provide clear contextual information that helps
  users understand when they need to take specific actions versus when configurations
  are automatically handled. Include deployment-specific details and maintain consistent
  cross-referencing syntax throughout.
repository: lobehub/lobe-chat
label: Documentation
language: Other
comments_count: 2
repository_stars: 65138
---

Documentation should provide clear contextual information that helps users understand when they need to take specific actions versus when configurations are automatically handled. Include deployment-specific details and maintain consistent cross-referencing syntax throughout.

When documenting configuration options, specify the conditions under which manual setup is required:

```markdown
| Environment Variable | Type | Description |
| -------------------- | ---- | ----------- |
| `NEXT_PUBLIC_ENABLE_NEXT_AUTH` | Required | Used to enable NextAuth service. Set to `1` to enable; changing this setting requires recompiling the application. Users deploying with the `lobehub/lobe-chat-database` image have this configuration added by default. |
```

For cross-references, use consistent linking syntax that matches the existing documentation structure:
```markdown
This configuration is done in the environment for each [model providers](/docs/self-hosting/environment-variables/model-provider).
```

This approach reduces user confusion by clearly indicating when manual intervention is needed and ensures documentation maintains professional consistency.