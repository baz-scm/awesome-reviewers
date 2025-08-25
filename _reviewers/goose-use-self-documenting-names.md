---
title: Use self-documenting names
description: Choose variable, function, and constant names that clearly express their
  purpose and eliminate the need for explanatory comments. Break down complex expressions
  into well-named intermediate variables rather than relying on comments to explain
  the logic.
repository: block/goose
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 19037
---

Choose variable, function, and constant names that clearly express their purpose and eliminate the need for explanatory comments. Break down complex expressions into well-named intermediate variables rather than relying on comments to explain the logic.

For example, instead of:
```typescript
// Use explicit hasEnvVars if provided, otherwise fall back to checking step3Content
const hasConfiguration = hasEnvVars !== undefined ? hasEnvVars : step3Content !== null;
```

Use descriptive intermediate variables:
```typescript
const hasConfigurationContent = step3Content !== null;
const shouldShowConfigurationSteps = hasEnvVars ?? hasConfigurationContent;
```

This principle also applies to extracting repeated string literals into named constants. Instead of using 'New Chat' multiple times throughout the code, define a constant like `DEFAULT_CHAT_TITLE = 'New Chat'` to make the intent clear and improve maintainability.