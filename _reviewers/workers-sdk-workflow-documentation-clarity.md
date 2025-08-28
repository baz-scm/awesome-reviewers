---
title: workflow documentation clarity
description: Ensure all workflow-related documentation, help text, and code comments
  use proper grammar and punctuation. Workflow systems involve complex orchestration,
  retries, and fault tolerance mechanisms that require clear, professional documentation
  for maintainability and developer understanding.
repository: cloudflare/workers-sdk
label: Temporal
language: TypeScript
comments_count: 2
repository_stars: 3379
---

Ensure all workflow-related documentation, help text, and code comments use proper grammar and punctuation. Workflow systems involve complex orchestration, retries, and fault tolerance mechanisms that require clear, professional documentation for maintainability and developer understanding.

Pay special attention to:
- Proper comma usage in lists and clauses
- Clear sentence structure in workflow descriptions
- Professional formatting of code comments explaining workflow behavior

Example of proper formatting:
```typescript
// You can optionally have a Workflow wait for additional data,
// human approval or an external webhook or HTTP request, before progressing.

// Help text should read:
// "For multi-step applications that automatically retry, persist state, and run for minutes, hours, days or weeks"
```

Well-documented workflows reduce onboarding time and prevent misunderstandings about complex temporal execution patterns.