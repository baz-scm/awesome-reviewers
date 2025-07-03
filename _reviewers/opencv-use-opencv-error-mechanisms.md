---
title: Use OpenCV error mechanisms
description: Always use OpenCV's built-in error handling mechanisms instead of C++
  exceptions or custom error handling. This ensures consistent error handling across
  the codebase and proper integration with OpenCV's error handling infrastructure.
repository: opencv/opencv
label: Error Handling
language: C++
comments_count: 6
repository_stars: 82865
---

Always use OpenCV's built-in error handling mechanisms instead of C++ exceptions or custom error handling. This ensures consistent error handling across the codebase and proper integration with OpenCV's error handling infrastructure.

Key guidelines:
1. Use CV_Assert() for input validation and preconditions
2. Use CV_Error() for runtime errors
3. Use CV_LOG_WARNING() for non-fatal issues
4. Return status codes instead of throwing exceptions

Example:
```cpp
void processImage(InputArray src, OutputArray dst, int param) {
    // Input validation
    CV_Assert(src.dims() <= 2 && src.channels() <= 4);
    CV_Assert(param > 0 && param < 100);

    // Runtime error handling
    if (!src.isContinuous())
        CV_Error(Error::StsBadArg, "Input array must be continuous");

    // Warning for non-fatal issues
    if (param < 10)
        CV_LOG_WARNING(NULL, "Parameter value < 10 may reduce accuracy");

    // Return false instead of throwing
    if (!processData())
        return false;
}
```
