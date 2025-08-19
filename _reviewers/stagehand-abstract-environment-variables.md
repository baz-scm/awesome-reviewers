---
title: abstract environment variables
description: Avoid directly referencing environment variables throughout your codebase.
  Instead, abstract them into named constants with sensible defaults at module boundaries.
  This improves readability, makes configuration explicit, and prevents scattered
  environment variable access.
repository: browserbase/stagehand
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 16443
---

Avoid directly referencing environment variables throughout your codebase. Instead, abstract them into named constants with sensible defaults at module boundaries. This improves readability, makes configuration explicit, and prevents scattered environment variable access.

Create constants that handle the environment variable logic once:

```typescript
// Good: Abstract with defaults
const DEFAULT_EVAL_MODELS = process.env.EVAL_MODELS 
  ? process.env.EVAL_MODELS.split(",") 
  : ["gpt-4o", "claude-3-5-sonnet-latest"];

const EXPERIMENTAL_EVAL_MODELS = process.env.EXPERIMENTAL_EVAL_MODELS
  ? process.env.EXPERIMENTAL_EVAL_MODELS.split(",")
  : [];

// Then reference the constants
const models = useExperimental ? EXPERIMENTAL_EVAL_MODELS : DEFAULT_EVAL_MODELS;

// Bad: Direct references scattered throughout
const models = process.env.EVAL_MODELS?.split(",") || ["gpt-4o", "claude-3-5-sonnet-latest"];
```

Remember that `process.env.VARIABLE` defaults to `undefined` when not present - avoid adding unnecessary `|| undefined` or required assertions (`!`) unless the variable is truly mandatory. Use descriptive constant names that clearly indicate their purpose and scope.