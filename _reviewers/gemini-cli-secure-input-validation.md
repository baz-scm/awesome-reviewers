---
title: Secure input validation
description: Always validate and sanitize user inputs, especially when constructing
  commands or file paths. Use established security libraries instead of implementing
  custom parsing logic, and implement proper validation that prevents attacks while
  avoiding false positives.
repository: google-gemini/gemini-cli
label: Security
language: TypeScript
comments_count: 6
repository_stars: 65062
---

Always validate and sanitize user inputs, especially when constructing commands or file paths. Use established security libraries instead of implementing custom parsing logic, and implement proper validation that prevents attacks while avoiding false positives.

Key practices:
- Use proven libraries for security-critical operations like shell escaping rather than rolling your own
- Implement secure command parsing that properly handles quoted arguments and special characters
- Validate file paths to prevent directory traversal attacks by ensuring resolved paths stay within allowed boundaries
- Balance security checks to prevent dangerous patterns without blocking legitimate use cases

Example of secure command parsing:
```typescript
// Instead of unsafe split
const parts = command.split(/\s+/); // Unsafe - doesn't handle quotes

// Use secure parsing
const parts = splitCommandSafely(command);
if (!parts) {
  return 'Command parsing failed: unmatched quotes';
}

// Validate path traversal
const rootDir = path.resolve(this.config.getTargetDir());
const resolvedDir = path.resolve(rootDir, params.directory);
if (!resolvedDir.startsWith(rootDir + path.sep) && resolvedDir !== rootDir) {
  return 'Directory traversal is not allowed. Path must be within the project root.';
}
```

This approach prevents injection attacks, handles edge cases properly, and maintains functionality while ensuring security.