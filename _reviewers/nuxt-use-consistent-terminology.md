---
title: Use consistent terminology
description: Prioritize consistent, clear, and beginner-friendly terminology throughout
  your codebase and documentation. Choose names that are intuitive for users rather
  than technically precise but confusing. Maintain consistency with established patterns
  and style guidelines.
repository: nuxt/nuxt
label: Naming Conventions
language: Markdown
comments_count: 7
repository_stars: 57769
---

Prioritize consistent, clear, and beginner-friendly terminology throughout your codebase and documentation. Choose names that are intuitive for users rather than technically precise but confusing. Maintain consistency with established patterns and style guidelines.

Key principles:
- **Favor clarity over technical accuracy**: Use `ViteConfig` instead of `UserConfig` when the context makes it clearer that it's Vite configuration
- **Use beginner-friendly terms**: Prefer "client-side" over "front-end" and "server-side" over "back-end" for accessibility
- **Maintain consistency**: Use "user interface" consistently instead of mixing with "UI", and follow established import patterns like `~/` over `@/`
- **Follow style guidelines**: Apply proper capitalization rules (e.g., "TypeScript-Friendly" following APA style, "vs" lowercase in "ESM vs CJS")
- **Match existing APIs**: When naming new parameters, consider existing patterns (e.g., `refreshEvery` to match native functions rather than `pollEvery`)

Example of good terminology consistency:
```typescript
// Good - clear and consistent
interface ViteConfig {
  clientSide: boolean;
  serverSide: boolean;
}

// Avoid - technically correct but less intuitive
interface UserConfig {
  frontEnd: boolean;
  backEnd: boolean;
}
```