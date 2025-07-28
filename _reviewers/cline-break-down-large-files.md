---
title: break down large files
description: Large files with multiple responsibilities should be broken down into
  focused, single-responsibility modules to improve maintainability and avoid tight
  coupling. When a file becomes difficult to navigate or contains unrelated functionality,
  extract logical components into separate files or classes.
repository: cline/cline
label: Code Style
language: TypeScript
comments_count: 8
repository_stars: 48299
---

Large files with multiple responsibilities should be broken down into focused, single-responsibility modules to improve maintainability and avoid tight coupling. When a file becomes difficult to navigate or contains unrelated functionality, extract logical components into separate files or classes.

Key indicators for refactoring:
- Files that are "very large" and hard to navigate
- Classes that inherit from others when composition would be cleaner
- Platform-specific code mixed with generic logic
- Functions that could be reused across multiple locations

Example refactoring approach:
```typescript
// Instead of a large BrowserSession.ts with everything:
// Break into focused modules:
// - ChromeExecutableManager.ts (for ensureChromiumExists, getDetectedChromePath)
// - BrowserConnectionManager.ts (for connection logic)
// - BrowserSession.ts (core session management only)

// Instead of inheritance when not needed:
export class OcaHandler extends LiteLlmHandler { // Avoid this
}

// Prefer composition:
export class OcaHandler {
  constructor(private authManager: OcaTokenManager) {}
}
```

When refactoring, make incremental changes - move existing code to new files without changing functionality simultaneously. Separate platform-specific code paths into dedicated modules (like host-providers) rather than mixing them with generic logic.