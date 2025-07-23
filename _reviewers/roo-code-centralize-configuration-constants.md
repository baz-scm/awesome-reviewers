---
title: Centralize configuration constants
description: Always centralize configuration constants in a shared location and import
  them rather than duplicating values across the codebase. This prevents drift between
  frontend and backend configurations, reduces errors from manual updates, and makes
  configuration changes easier to manage.
repository: RooCodeInc/Roo-Code
label: Configurations
language: TSX
comments_count: 3
repository_stars: 17288
---

Always centralize configuration constants in a shared location and import them rather than duplicating values across the codebase. This prevents drift between frontend and backend configurations, reduces errors from manual updates, and makes configuration changes easier to manage.

For example, instead of:

```typescript
// In UI component
<input
  type="range"
  min="0"
  max="1" 
  step="0.05"
  value={codebaseIndexConfig.codebaseIndexSearchMinScore || 0.4}
/>

// In another file
const defaultMinScore = 0.4;
```

Do this:

```typescript
// In shared constants file
export const SEARCH_MIN_SCORE = 0.4;

// In UI component
import { SEARCH_MIN_SCORE } from "@/constants/config";

<input
  type="range"
  min="0"
  max="1"
  step="0.05"
  value={codebaseIndexConfig.codebaseIndexSearchMinScore || SEARCH_MIN_SCORE}
/>
```

This approach also applies to default values derived from dynamic sources, where you should establish a clear fallback chain:

```typescript
const displayValue = value ?? modelInfo?.maxTokens ?? DEFAULT_MAX_TOKENS
```

When centralizing configuration constants:
1. Create dedicated files for related configuration constants
2. Use descriptive names that indicate purpose and context
3. Document expected value ranges or formats when needed
4. Consider using TypeScript const assertions for added type safety