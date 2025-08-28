---
title: Use KJ_UNWRAP_OR pattern
description: When handling potentially null values from functions like `tryParse()`
  or `tryCast()`, avoid the pattern of checking for null/none and then immediately
  using `KJ_ASSERT_NONNULL` or `JSG_REQUIRE_NONNULL`. This creates redundant checks
  that make code harder to read and understand.
repository: cloudflare/workerd
label: Null Handling
language: Other
comments_count: 3
repository_stars: 6989
---

When handling potentially null values from functions like `tryParse()` or `tryCast()`, avoid the pattern of checking for null/none and then immediately using `KJ_ASSERT_NONNULL` or `JSG_REQUIRE_NONNULL`. This creates redundant checks that make code harder to read and understand.

Instead, use the `KJ_UNWRAP_OR` macro to handle the null case directly and extract the value in one step. This pattern is cleaner, more efficient, and eliminates the cognitive overhead of tracking whether a value can be null.

**Problematic pattern:**
```cpp
auto currentUrl = jsg::Url::tryParse(base.asPtr());
if (currentUrl == kj::none) {
  auto exception = JSG_KJ_EXCEPTION(FAILED, TypeError, "Invalid current URL");
  return js.rejectedPromise<jsg::Ref<Response>>(kj::mv(exception));
}
// Later: KJ_ASSERT_NONNULL(currentUrl) - redundant since we already checked
```

**Preferred pattern:**
```cpp
auto currentUrl = KJ_UNWRAP_OR(jsg::Url::tryParse(base.asPtr()), {
  auto exception = JSG_KJ_EXCEPTION(FAILED, TypeError, "Invalid current URL");
  return js.rejectedPromise<jsg::Ref<Response>>(kj::mv(exception));
});
// Now currentUrl can be used directly without null checks
```

This approach makes the code more readable by eliminating the need to verify that null checks guarantee non-null values later in the code.