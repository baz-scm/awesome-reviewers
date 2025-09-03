---
title: Use centralized model state
description: Always access AI model information, parameters, and configuration through
  centralized state management rather than direct access or hardcoded values. This
  ensures consistency, maintainability, and proper separation of concerns when working
  with AI models.
repository: menloresearch/jan
label: AI
language: TSX
comments_count: 2
repository_stars: 37620
---

Always access AI model information, parameters, and configuration through centralized state management rather than direct access or hardcoded values. This ensures consistency, maintainability, and proper separation of concerns when working with AI models.

For model access, use established state management patterns:
```typescript
// Good: Use centralized state
const model = currentActiveModel

// Avoid: Direct model access
const model = message.model
```

For model parameters (like llama.cpp settings), define constraints centrally rather than scattered throughout components:
```typescript
// Good: Centralized parameter definitions
const llamaParams = {
  temperature: { min: 0, max: 2, step: 0.1 },
  maxTokens: { min: 1, max: 4096, step: 1 }
}

// Avoid: Hardcoded values in components
<SliderRightPanel min={0} max={100} step={1} />
```

This approach prevents inconsistencies, makes parameter updates easier, and provides a single source of truth for AI model configuration across the application.