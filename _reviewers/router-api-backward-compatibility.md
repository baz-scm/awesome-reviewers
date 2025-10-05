---
title: API backward compatibility
description: When updating existing APIs, maintain backward compatibility by deprecating
  old options rather than introducing breaking changes. Add new properties while keeping
  old ones functional, marking them as deprecated to guide migration without forcing
  immediate updates.
repository: TanStack/router
label: API
language: Markdown
comments_count: 4
repository_stars: 11590
---

When updating existing APIs, maintain backward compatibility by deprecating old options rather than introducing breaking changes. Add new properties while keeping old ones functional, marking them as deprecated to guide migration without forcing immediate updates.

Key principles:
- Never make previously optional parameters required without maintaining the old signature
- When renaming API properties, keep the old names working alongside new ones
- Mark deprecated options clearly in documentation but continue supporting them
- Provide migration paths that don't require immediate code changes

Example approach for API updates:
```tsx
// Instead of breaking change:
// OLD: { blockerFn?: Function }
// NEW: { shouldBlockFn: Function } // ❌ Breaking!

// Use backward-compatible approach:
type UseBlockerOpts = {
  shouldBlockFn: BlockerFn // New preferred option
  enableBeforeUnload?: boolean
} & {
  blockerFn?: LegacyBlockerFn // Keep old option, mark deprecated
  condition?: boolean // Keep old option, mark deprecated
}
```

This approach ensures existing code continues working while encouraging adoption of improved APIs. Keep public API surfaces minimal by avoiding exposure of internal types that change frequently, focusing documentation on stable, user-facing interfaces only.