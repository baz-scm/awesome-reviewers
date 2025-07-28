---
title: Use appropriate logging levels
description: Use console.debug() for debug information instead of console.log() to
  prevent cluttering user-facing output. Debug information should be hidden from normal
  users but available when debugging is enabled.
repository: google-gemini/gemini-cli
label: Logging
language: TypeScript
comments_count: 2
repository_stars: 65062
---

Use console.debug() for debug information instead of console.log() to prevent cluttering user-facing output. Debug information should be hidden from normal users but available when debugging is enabled.

When logging information that is primarily useful for developers or troubleshooting, use console.debug() rather than console.log(). This ensures that users don't see unnecessary technical details during normal operation, while still making the information available when needed for debugging.

Example:
```typescript
// Bad - users will see this debug information
console.log("buildImangeName:imageName ", imageName);
console.log(`Discovered tool: ${funcDecl.name}`);

// Good - debug information is properly categorized
console.debug("buildImangeName:imageName ", imageName);
console.debug(`Discovered tool: ${funcDecl.name}`);
```

This practice improves user experience by keeping the console output clean while maintaining valuable debugging capabilities for developers.