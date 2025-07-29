---
title: comprehensive test assertions
description: Write test assertions that are both comprehensive and maintainable. Ensure
  all relevant fields and behaviors are validated, while using generic matchers where
  appropriate to reduce brittleness.
repository: apache/kafka
label: Testing
language: Other
comments_count: 2
repository_stars: 30575
---

Write test assertions that are both comprehensive and maintainable. Ensure all relevant fields and behaviors are validated, while using generic matchers where appropriate to reduce brittleness.

**Comprehensive Coverage**: Assert all relevant fields in response objects, not just error codes. For example, when testing fetch responses, verify highWatermark, logStartOffset, and other expected fields:

```scala
// Instead of only checking error
assertEquals(Errors.NONE, responses(topicIdPartition).error)

// Also verify other relevant fields
assertEquals(Errors.NONE, responses(topicIdPartition).error)
assertEquals(highWatermark, responses(topicIdPartition).highWatermark)
assertEquals(leaderLogStartOffset, responses(topicIdPartition).logStartOffset)
```

**Maintainable Assertions**: Use generic matchers like `anyLong()` instead of hardcoded values when the specific value isn't critical to the test logic:

```scala
// Instead of brittle specific values
verify(coordinator, times(0)).updateLastWrittenOffset(0)
verify(coordinator, times(1)).updateLastWrittenOffset(2)
verify(coordinator, times(1)).updateLastWrittenOffset(5)

// Use generic matchers when appropriate
verify(coordinator, times(0)).updateLastWrittenOffset(anyLong())
verify(coordinator, times(3)).updateLastWrittenOffset(anyLong())
```

This approach ensures tests validate the complete behavior while remaining resilient to implementation changes that don't affect the core functionality being tested.