---
title: PascalCase constants
description: Use a consistent PascalCase naming convention for constants (especially
  exported ones). Avoid mixed styles like snake_case, and keep acronym casing consistent
  (e.g., API).
repository: infiniflow/ragflow
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 80174
---

Use a consistent PascalCase naming convention for constants (especially exported ones). Avoid mixed styles like snake_case, and keep acronym casing consistent (e.g., API).

When you rename a constant to match the standard, update all references/usages together (including “lite”/variant constants) to stay DRY and prevent mismatches.

Example:
```ts
// ❌ Avoid snake_case
// const api_host = `/v1`;

// ✅ Prefer PascalCase for constants, consistent acronym casing
const webAPI = `/v1`;

export const MarkdownRemarkPlugins = [remarkGfm, remarkMath, remarkBreaks];
export const MarkdownRemarkPluginsLite = [remarkGfm, remarkBreaks];
```