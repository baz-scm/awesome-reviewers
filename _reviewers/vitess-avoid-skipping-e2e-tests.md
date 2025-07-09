---
title: Avoid skipping e2e tests
description: Do not use the `skip_e2e` flag to bypass end-to-end tests that fail.
  Instead, fix the test implementation by providing appropriate test data or modifying
  the test to make it pass correctly. This maintains the integrity of the test suite
  and ensures that code changes are properly validated.
repository: vitessio/vitess
label: Testing
language: Json
comments_count: 2
repository_stars: 19815
---

Do not use the `skip_e2e` flag to bypass end-to-end tests that fail. Instead, fix the test implementation by providing appropriate test data or modifying the test to make it pass correctly. This maintains the integrity of the test suite and ensures that code changes are properly validated.

When adding new test cases, especially those involving complex operations like joins that require specific verification conditions, include the necessary sample data:

```go
// Instead of this:
{
  "comment": "Between clause on a binary vindex field with values from a different table",
  "query": "select s.oid,s.col1, se.colb from sales s join sales_extra se on s.col1 = se.cola where s.oid between se.start and se.end",
  "plan": {
    // Plan details...
  },
  "skip_e2e": true  // DON'T DO THIS
}

// Do this:
// 1. Add necessary sample data
// Example: Add data loading for test tables
// 2. Remove the skip_e2e flag
{
  "comment": "Between clause on a binary vindex field with values from a different table",
  "query": "select s.oid,s.col1, se.colb from sales s join sales_extra se on s.col1 = se.cola where s.oid between se.start and se.end",
  "plan": {
    // Plan details...
  }
  // No skip_e2e flag - test will run
}
```

This approach ensures comprehensive test coverage and helps catch issues that might otherwise go undetected in production code. Maintaining a policy of not adding `skip_e2e` flags to new tests encourages better test design and more robust code.