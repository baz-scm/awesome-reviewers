---
title: Decouple tests from implementation
description: Tests tightly coupled to implementation details break easily when the
  implementation changes, creating maintenance burden and reducing test reliability.
  Write tests that validate behavior rather than specific implementation details.
repository: continuedev/continue
label: Testing
language: TypeScript
comments_count: 5
repository_stars: 27819
---

Tests tightly coupled to implementation details break easily when the implementation changes, creating maintenance burden and reducing test reliability. Write tests that validate behavior rather than specific implementation details.

To avoid implementation coupling:

1. Import constants from source rather than redefining them:

```typescript
// GOOD
import { DEFAULT_GIT_DIFF_LINE_LIMIT } from "./viewDiff";

test("viewDiff should truncate diffs exceeding line limit", async () => {
  const largeInput = Array(DEFAULT_GIT_DIFF_LINE_LIMIT + 1).fill("test line");
  // ...
});

// BAD
test("viewDiff should truncate diffs exceeding line limit", async () => {
  const DEFAULT_GIT_DIFF_LINE_LIMIT = 5000; // Duplicated constant
  // Test will break if implementation changes the limit
  // ...
});
```

2. Verify assumptions instead of hardcoding expected values:

```typescript
// GOOD
test("should use the default TTL value", () => {
  const anthropic = new Anthropic({/* config */});
  const defaultTtl = anthropic.getDefaultTtl(); // Get actual implementation value
  
  const result = anthropic.convertMessages(messages);
  expect(result[0].content[0].cache_control.ttl).toBe(defaultTtl);
});

// BAD
test("should use default TTL when not specified", () => {
  // Assumes '5m' is the default without verification
  expect(result.content[0].cache_control.ttl).toBe("5m");
});
```

3. Test behavior and outcomes instead of internal structure:

```typescript
// GOOD - Tests behavior without assuming structure
test("should contain expected rule names", () => {
  const applicableRules = getApplicableRules();
  expect(getRuleNames(applicableRules)).toContain("Global Rule");
});

// BAD - Tightly coupled to structure
test("should contain expected rule names", () => {
  const applicableRules = getApplicableRules();
  expect(applicableRules.map(r => r.rule.name)).toContain("Global Rule");
});
```

When mocking, verify the right parameters are passed rather than just counting calls. This ensures tests remain valid even when implementation details change.