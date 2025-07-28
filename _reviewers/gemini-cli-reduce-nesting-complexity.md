---
title: reduce nesting complexity
description: Prefer early returns, guard clauses, and helper method extraction to
  reduce nesting levels and improve code readability. Deep nesting makes code harder
  to follow and understand.
repository: google-gemini/gemini-cli
label: Code Style
language: TypeScript
comments_count: 7
repository_stars: 65062
---

Prefer early returns, guard clauses, and helper method extraction to reduce nesting levels and improve code readability. Deep nesting makes code harder to follow and understand.

**Apply early returns to eliminate unnecessary nesting:**
```typescript
// Instead of:
if (config) {
  const promptCommands: SlashCommand[] = [];
  // ... more nested logic
}

// Use early return:
if (!config) { 
  return promptCommands; 
}
const promptCommands: SlashCommand[] = [];
// ... logic at top level
```

**Extract complex conditionals into helper methods:**
```typescript
// Instead of nested ternary:
const effectiveAuthType = configuredAuthType || 
  (process.env.GOOGLE_GENAI_USE_GCP === 'true'
    ? AuthType.USE_VERTEX_AI
    : process.env.GEMINI_API_KEY
      ? AuthType.USE_GEMINI
      : undefined);

// Use switch or helper method for clarity
```

**Replace magic numbers with named constants:**
```typescript
// Instead of:
await new Promise((res) => setTimeout(res, 200));

// Use:
const PROCESS_KILL_TIMEOUT_MS = 200;
await new Promise((res) => setTimeout(res, PROCESS_KILL_TIMEOUT_MS));
```

**Extract complex logic into focused helper methods** rather than embedding it inline. This keeps the main function readable and allows for better testing and reuse.