---
title: Canonical Identifier Semantics
description: When code maps or normalizes external identifiers (tool names, locale
  tags, etc.), it must preserve the identifier’s real semantics and use canonical
  names.
repository: nousresearch/hermes-agent
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 221948
---

When code maps or normalizes external identifiers (tool names, locale tags, etc.), it must preserve the identifier’s real semantics and use canonical names.

**Standards**
- **Use canonical forms for identifiers and fixtures**: if an external system uses a specific naming pattern, mirror that pattern in tests/fixtures (e.g., `mcp__<server>__<tool>`), and only transform for *display* when needed.
- **Avoid incorrect “helpful” aliasing**: alias maps (e.g., locale tag normalization) must reflect the true meaning of each tag. Do not silently route unrelated tags to the wrong category.
- **Make normalization explicitly semantic-safe**: if normalization changes representation, document and enforce that it does not change semantics (unless the mapping is correct).
- **Add regression tests for the canonical input**: ensure tests include the real/canonical external identifiers so the behavior matches production naming.

**Example pattern (display-only normalization)**
```ts
// Canonical external identifier (real MCP name)
type McpToolName = 'mcp__filesystem__write_file'

function displayTitle(toolName: McpToolName): string {
  // Safe display-only transformation; semantics preserved
  if (toolName === 'mcp__filesystem__write_file') return 'write_file'
  return toolName
}
```

**Example anti-pattern (semantic-unsafe aliasing)**
```ts
// ❌ Incorrect: Belarusian/Ukrainian/Kazakh tags mapped to Russian UI
const LOCALE_ALIASES: Record<string, 'ru'> = {
  be: 'ru',
  uk: 'ru',
  kk: 'ru'
}
// Fix by removing/correcting those mappings.
```