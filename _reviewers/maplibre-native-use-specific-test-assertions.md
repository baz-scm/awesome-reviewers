---
title: Use specific test assertions
description: Always use the most specific test assertion method available for your
  test case rather than generic assertions. Specific assertions provide better error
  messages and make test failures easier to debug.
repository: maplibre/maplibre-native
label: Testing
language: C++
comments_count: 2
repository_stars: 1411
---

Always use the most specific test assertion method available for your test case rather than generic assertions. Specific assertions provide better error messages and make test failures easier to debug.

For string comparisons, use `EXPECT_STREQ` instead of `ASSERT_TRUE` with string equality:

```cpp
// Instead of:
ASSERT_TRUE(json == testValue);

// Use:
EXPECT_STREQ(json.c_str(), testValue.c_str());
```

For exception testing, use `EXPECT_THROW` to properly verify exceptions instead of manually catching them:

```cpp
// Instead of:
try {
    lru.evict();
    // Test will pass even if no exception is thrown
} catch (...) {
    // ...
}

// Use:
EXPECT_THROW(lru.evict(), SomeExceptionType);
```

Specific assertions like these will print the actual and expected values when tests fail, making debugging much faster and providing clearer failure messages in test reports.