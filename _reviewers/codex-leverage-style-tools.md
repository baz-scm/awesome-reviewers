---
title: Leverage style tools
description: Maintain consistent code style by using and respecting the project's
  established formatting tools and patterns. Run linters and formatters (`pnpm run
  format`, `pnpm run lint`) before committing code. Organize logical expressions for
  clarity and consistency, and prefer language constructs that work well with static
  analysis tools.
repository: openai/codex
label: Code Style
language: TypeScript
comments_count: 4
repository_stars: 31275
---

Maintain consistent code style by using and respecting the project's established formatting tools and patterns. Run linters and formatters (`pnpm run format`, `pnpm run lint`) before committing code. Organize logical expressions for clarity and consistency, and prefer language constructs that work well with static analysis tools.

For example, maintain symmetry in related conditional blocks:

```typescript
// GOOD: Organize conditions symmetrically and logically
if (
  (key["meta"] || key["ctrl"] || key["alt"]) &&
  (key["backspace"] || input === "\x7f") &&
  !key["shift"]
) {
  this.deleteWordLeft();
}

// AVOID: Asymmetrical or nested conditions that are harder to parse
if (
  (key["meta"] || key["ctrl"] || key["alt"]) &&
  (key["backspace"] || input === "\x7f" || (key["delete"] && !key["shift"]))
) {
  this.deleteWordLeft();
}
```

Use language constructs that leverage static analysis, like switch statements for exhaustive checking of enum values, even when it might seem easier to convert to if/else statements. This ensures that when new enum variants are added, existing code will be flagged for updates.