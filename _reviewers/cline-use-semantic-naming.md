---
title: use semantic naming
description: Choose variable, function, and type names that clearly communicate their
  purpose and meaning without requiring additional context or comments. Names should
  be self-documenting and unambiguous to future developers.
repository: cline/cline
label: Naming Conventions
language: TypeScript
comments_count: 5
repository_stars: 48299
---

Choose variable, function, and type names that clearly communicate their purpose and meaning without requiring additional context or comments. Names should be self-documenting and unambiguous to future developers.

Replace generic or unclear identifiers with descriptive alternatives:
- Use specific, meaningful names instead of generic terms like "preview" when "local" better describes the environment
- Prefer boolean variables with clear intent like `enableExpandedMcpPanelState` over ambiguous string states like `"collapsed" | "expanded"`
- Replace magic numbers with named constants that explain their purpose: `const CONTEXT_EXPANSION_LINES = 3` instead of hardcoded `3`
- Avoid hardcoded strings like `"claude_message.json"` - use descriptive constants or derive from existing naming conventions

For complex types, ensure the type structure is self-explanatory:
```typescript
// Instead of unclear typing
private contextHistoryUpdates: Map<number, [number, Map<number, ContextUpdate[]>]>

// Use descriptive types
private contextHistoryUpdates: Map<number, [EditType, Map<number, ContextUpdate[]>]>
```

When names become long for clarity, prioritize understanding over brevity. A longer, clear name is preferable to a short, ambiguous one that requires documentation to understand.