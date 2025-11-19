---
title: validate configuration values
description: Always validate configuration values at runtime and provide clear, actionable
  error messages when invalid combinations are detected. This prevents runtime failures
  and guides users toward correct configuration.
repository: nrwl/nx
label: Configurations
language: TypeScript
comments_count: 6
repository_stars: 27518
---

Always validate configuration values at runtime and provide clear, actionable error messages when invalid combinations are detected. This prevents runtime failures and guides users toward correct configuration.

Key validation practices:
- Check environment variables against allowed values before use
- Validate configuration combinations that are mutually incompatible  
- Provide specific error messages that explain the problem and suggest solutions
- Use runtime checks rather than relying on schema validation alone

Example from environment variable validation:
```typescript
if (
  !args.outputStyle && 
  process.env.NX_DEFAULT_OUTPUT_STYLE && 
  choices.includes(process.env.NX_DEFAULT_OUTPUT_STYLE as OutputStyle)
) {
  args.outputStyle = process.env.NX_DEFAULT_OUTPUT_STYLE;
}
```

Example from configuration combination validation:
```typescript
if (usesVersionPlaceholder && hasSkipVersionActions) {
  throw new Error(
    `Release group "${groupName}" configures "skipVersionActions" but its docker version scheme contains the "{versionActionsVersion}" placeholder which cannot be resolved without version actions. Remove "skipVersionActions" or remove the placeholder from the scheme.`
  );
}
```

This approach catches configuration errors early, provides clear guidance for resolution, and prevents confusing runtime failures that are difficult to debug.