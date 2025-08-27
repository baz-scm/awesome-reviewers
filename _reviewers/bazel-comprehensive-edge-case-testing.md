---
title: comprehensive edge case testing
description: Write comprehensive tests that cover edge cases and platform-specific
  scenarios to uncover underlying implementation issues rather than masking them with
  workarounds. When encountering failures, investigate the root cause through targeted
  testing before implementing fallback mechanisms.
repository: bazelbuild/bazel
label: Testing
language: Other
comments_count: 2
repository_stars: 24489
---

Write comprehensive tests that cover edge cases and platform-specific scenarios to uncover underlying implementation issues rather than masking them with workarounds. When encountering failures, investigate the root cause through targeted testing before implementing fallback mechanisms.

For platform-specific issues, add integration tests that run on the affected platforms:
```cpp
// Instead of adding fallbacks like:
if (!IsReadableFile(*result)) {
  // fallback logic
}

// Add platform-specific integration tests to investigate the root cause
```

For complex functionality, test edge cases systematically:
```java
// Test comprehensive scenarios like:
// * UTF-16 strings with non-ASCII BMP characters
// * UTF-16 strings with surrogate pairs  
// * Latin1-hack strings with invalid UTF-8
// * Unpaired surrogates in various positions
```

This approach often reveals bugs in existing implementations that would otherwise remain hidden. As noted in one review: "This was both a nightmare and super helpful as the previous implementation had a number of bugs." Comprehensive testing serves as both quality assurance and debugging tool, helping teams understand the true behavior of their code rather than working around symptoms.