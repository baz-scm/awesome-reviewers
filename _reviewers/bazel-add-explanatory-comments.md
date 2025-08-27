---
title: Add explanatory comments
description: Add explanatory comments and documentation for complex logic, non-obvious
  code behavior, method parameters, and API functionality to improve code readability
  and maintainability.
repository: bazelbuild/bazel
label: Documentation
language: Java
comments_count: 11
repository_stars: 24489
---

Add explanatory comments and documentation for complex logic, non-obvious code behavior, method parameters, and API functionality to improve code readability and maintainability.

This applies to several scenarios:
- Complex algorithms or logic that aren't immediately clear from the code
- Boolean parameters or magic values that need explanation
- Method behavior that has side effects or special conditions
- Constructor parameters and their roles
- API methods missing complete documentation

Examples:
```java
// Comment explaining complex logic
if (entry.getKey() == null) {
  // Remove entry when key is null - using value as the key to remove
  normalizedEntries.remove(entry.getValue());
}

// Comment explaining boolean parameter meaning
SpawnInputExpander spawnInputExpander = new SpawnInputExpander(execRoot, /* relativeToExecRoot= */ false);

// Complete method documentation
/**
 * Renames the file or directory from src to dst.
 * Parent directories are created as needed. If the target already exists, it will be overwritten.
 * 
 * @param clientEnv the client environment variables used for subprocess execution
 */
```

The goal is to make code self-documenting through clear comments that explain the "why" behind non-obvious implementation decisions, parameter meanings, and expected behavior.