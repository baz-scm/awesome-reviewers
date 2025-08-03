---
title: Write resilient test assertions
description: Write test assertions that are resilient to implementation changes by
  focusing on behavior rather than implementation details. Avoid exact matches when
  partial or behavioral assertions would suffice.
repository: RooCodeInc/Roo-Code
label: Testing
language: TypeScript
comments_count: 5
repository_stars: 17288
---

Write test assertions that are resilient to implementation changes by focusing on behavior rather than implementation details. Avoid exact matches when partial or behavioral assertions would suffice.

Key practices:
1. Use flexible matchers instead of exact equality
2. Focus on behavior over implementation details
3. Test for presence of required properties rather than exact object shape

Example - Instead of brittle exact matching:
```typescript
// ❌ Brittle - breaks if new options are added
expect(options).toEqual({ 
  preview: false, 
  viewColumn: vscode.ViewColumn.Active 
})

// ✅ Resilient - verifies required properties
expect(options).toEqual(expect.objectContaining({ 
  preview: false,
  viewColumn: vscode.ViewColumn.Active 
}))
```

For token counting or similar approximate values:
```typescript
// ❌ Brittle - breaks if tokenizer changes slightly
expect(tokenCount).toBe(14)

// ✅ Resilient - verifies reasonable range
expect(tokenCount).toBeGreaterThan(12)
expect(tokenCount).toBeLessThan(16)
```

This approach:
- Reduces test maintenance as implementation details change
- Focuses tests on behavioral requirements
- Makes tests more reliable and meaningful
- Avoids over-mocking that tests the mocks rather than the code