---
title: Respect existing configurations
description: When integrating with external services or tools, design your configuration
  options to respect users' existing environment settings rather than overriding them
  with hardcoded defaults. This ensures your tool works seamlessly within various
  environments and avoids disrupting users' workflows.
repository: oven-sh/bun
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 79093
---

When integrating with external services or tools, design your configuration options to respect users' existing environment settings rather than overriding them with hardcoded defaults. This ensures your tool works seamlessly within various environments and avoids disrupting users' workflows.

Key practices:
1. Use environment-aware defaults that fall back to system conventions when no explicit value is provided
2. Apply configuration parameters consistently throughout the codebase
3. Use correct references to external resources

**Example 1:** For AWS CLI integration, omit the `--profile` flag when no profile is specified rather than hardcoding "default":

```typescript
// ❌ Bad: Hardcoding a default profile name
profile: Flags.string({
  description: "The AWS CLI profile to use.",
  multiple: false,
  default: "default", // Forces "default" even if user has AWS_PROFILE set
})

// ✅ Good: Make profile optional and apply it conditionally
profile: Flags.string({
  description: "The AWS CLI profile to use.",
  multiple: false,
  required: false,
})

// Then in code:
if (profile) {
  // Apply profile parameter consistently to all AWS commands
  this.#aws(["command", "--profile", profile]);
}
```

**Example 2:** Ensure external resource references are correct and complete:

```json
// ❌ Bad: Incomplete GitHub issues URL
"bugs": "https://github.com/oven-sh/issues"

// ✅ Good: Complete URL to the repository's issues page
"bugs": "https://github.com/oven-sh/bun/issues"
```

Following these practices helps users integrate your tool with their existing environment without unexpected side effects or configuration conflicts.