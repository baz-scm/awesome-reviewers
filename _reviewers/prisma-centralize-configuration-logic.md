---
title: Centralize configuration logic
description: Avoid scattering configuration defaults, validation, and loading logic
  across multiple functions. Instead, centralize these concerns in dedicated configuration
  modules or at the entry points of your application.
repository: prisma/prisma
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 42967
---

Avoid scattering configuration defaults, validation, and loading logic across multiple functions. Instead, centralize these concerns in dedicated configuration modules or at the entry points of your application.

**Problems with scattered configuration:**
- Default values redefined in multiple places lead to inconsistency
- Configuration loading logic duplicated across different modules
- Harder to maintain and debug configuration-related issues

**Best practices:**
1. **Centralize defaults at entry level** - Define default values once at the top-level configuration rather than in each function that needs them
2. **Extract configuration logic into dedicated functions** - Move complex configuration loading and validation into separate, testable functions
3. **Consolidate environment variable handling** - Handle environment variable loading in a single place rather than scattered throughout the codebase

**Example of the problem:**
```typescript
// Scattered defaults - AVOID
function buildClient({ target = 'nodejs' }) { /* ... */ }
function generateClient({ target = 'nodejs' }) { /* ... */ }
function processConfig({ target = 'nodejs' }) { /* ... */ }
```

**Better approach:**
```typescript
// Centralized configuration - PREFER
const DEFAULT_CONFIG = {
  target: 'nodejs',
  // other defaults...
};

function buildClient({ target = DEFAULT_CONFIG.target }) { /* ... */ }
function generateClient(options = DEFAULT_CONFIG) { /* ... */ }
```

This approach makes configuration changes easier to manage, reduces the risk of inconsistent defaults, and improves code maintainability by having a single source of truth for configuration values.