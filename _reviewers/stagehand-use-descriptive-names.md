---
title: Use descriptive names
description: Choose descriptive, domain-specific names that clearly communicate intent
  and prevent confusion. Avoid generic names when more specific alternatives exist,
  especially when working alongside similar types or concepts from external libraries.
repository: browserbase/stagehand
label: Naming Conventions
language: TypeScript
comments_count: 5
repository_stars: 16443
---

Choose descriptive, domain-specific names that clearly communicate intent and prevent confusion. Avoid generic names when more specific alternatives exist, especially when working alongside similar types or concepts from external libraries.

Key principles:
- Prefix with domain/library name when extending or wrapping external types (e.g., `StagehandPage` instead of `Page` to distinguish from Playwright's `Page`)
- Use semantically clear parameter names (e.g., `systemPrompt` instead of `instructions`)
- Create custom types with descriptive names (e.g., `StagehandContainer` for `HTMLElement | Window`)
- Add suffixes like `Schema` to distinguish type definitions from runtime values

Example:
```typescript
// Avoid generic names that could cause confusion
export interface Page extends PlaywrightPage { ... }

// Use descriptive, domain-specific names
export interface StagehandPage extends PlaywrightPage { ... }

// Avoid ambiguous parameter names
function configure(instructions?: string) { ... }

// Use semantically clear names
function configure(systemPrompt?: string) { ... }
```

This approach makes code self-documenting and reduces cognitive load when working with multiple similar concepts or external dependencies.