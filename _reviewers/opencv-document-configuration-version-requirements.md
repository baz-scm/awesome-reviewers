---
title: Document configuration version requirements
description: Make build configuration options explicit and document their version
  dependencies. When introducing configuration parameters that are version-specific,
  clearly indicate compatibility requirements and provide command-line options to
  make constraints optional when appropriate.
repository: opencv/opencv
label: Configurations
language: Python
comments_count: 2
repository_stars: 82865
---

Make build configuration options explicit and document their version dependencies. When introducing configuration parameters that are version-specific, clearly indicate compatibility requirements and provide command-line options to make constraints optional when appropriate.

For example, instead of hardcoding checks or settings:

```python
# Not recommended: Hardcoded check with no option to disable
check_have_ipp_flag(os.path.join(builder.libdest, "CMakeVars.txt"))

# Better approach: Make the check configurable
if args.strict_dependencies:
    check_have_ipp_flag(os.path.join(builder.libdest, "CMakeVars.txt"))

# When defining version-specific configurations, document requirements
# and use proper syntax
ABI("3", "arm64-v8a", None, 21, cmake_vars=dict(
    # Supported in Android NDK r27 and higher, ignored in earlier versions
    ANDROID_SUPPORT_FLEXIBLE_PAGE_SIZES='ON'
))
```

This approach ensures that configuration options remain flexible while clearly communicating version requirements to developers, preventing unexpected behavior across different environments.
