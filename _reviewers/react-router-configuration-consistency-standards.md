---
title: configuration consistency standards
description: Ensure configuration options, flags, and environment settings are handled
  consistently across all commands and modules. This includes supporting the same
  configuration flags across CLI commands, using standardized approaches for environment
  detection, and implementing clear precedence rules.
repository: remix-run/react-router
label: Configurations
language: TypeScript
comments_count: 6
repository_stars: 55270
---

Ensure configuration options, flags, and environment settings are handled consistently across all commands and modules. This includes supporting the same configuration flags across CLI commands, using standardized approaches for environment detection, and implementing clear precedence rules.

Key principles:
- Support configuration flags consistently across all CLI commands (like `--config` flag)
- Use build-time constants (`__DEV__`) instead of runtime environment checks (`process.env.NODE_ENV`) for library code
- Implement clear precedence rules where explicit parameters override inferred configuration
- Provide informative error messages that guide users toward solutions
- Calculate derived configuration flags using consistent logic

Example of good configuration precedence:
```typescript
function resolveRootDirectory(root?: string, flags?: { config?: string }) {
  if (root) {
    return path.resolve(root); // Explicit root takes precedence
  }
  // Fall back to inferring from config file location
  return inferRootFromConfig(flags?.config);
}
```

Example of consistent environment handling:
```typescript
// Good: Build-time constant for libraries
if (__DEV__ && !alreadyWarned[message]) {
  console.warn(message);
}

// Good: Runtime environment for CLI tools
process.env.NODE_ENV = process.env.NODE_ENV ?? 
  (command === "dev" ? "development" : "production");
```

This ensures predictable behavior and reduces confusion when the same configuration concepts are used in different parts of the system.