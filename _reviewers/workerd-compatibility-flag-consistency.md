---
title: compatibility flag consistency
description: Ensure compatibility flags follow consistent naming conventions, use
  explicit typing, and maintain proper usage patterns throughout the codebase. Compatibility
  flags should use descriptive, version-specific names that accurately reflect their
  purpose and lifecycle.
repository: cloudflare/workerd
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 6989
---

Ensure compatibility flags follow consistent naming conventions, use explicit typing, and maintain proper usage patterns throughout the codebase. Compatibility flags should use descriptive, version-specific names that accurately reflect their purpose and lifecycle.

**Naming Convention:**
- Use systematic versioning for EOL flags (e.g., `remove_nodejs_compat_eol_v22` for even releases)
- Follow hierarchical flag relationships where odd-numbered versions are implied by the next even-numbered version
- Use specific flag names rather than generic terms (e.g., `jsWeakRef` instead of "a specific flag")

**Type Safety:**
- Define explicit interfaces for compatibility flags rather than using generic `Record<string, boolean>`
- Consider auto-generating flag definitions from source files to avoid manual maintenance
- Use `Cloudflare.compatibilityFlags` consistently instead of alternative approaches

**Documentation:**
- Document flag interactions and dependencies, especially when flags affect each other
- Include examples showing which flags should or should not be used together
- Clearly state when flags are intentionally omitted and provide alternatives

**Example:**
```typescript
// Good: Explicit flag usage with clear naming
if (!Cloudflare.compatibilityFlags.remove_nodejs_compat_eol_v22) {
  // Implementation for Node.js compatibility
}

// Good: Document flag interactions
// Note: The disallow_importable_env flag should NOT be set 
// when using this feature as it prevents env access
```

This ensures configuration management remains maintainable, predictable, and well-documented as the system evolves.