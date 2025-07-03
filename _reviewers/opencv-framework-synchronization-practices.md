---
title: Framework synchronization practices
description: 'When implementing concurrent code, always use the framework''s provided
  synchronization primitives rather than direct language features. This ensures compatibility
  across all build configurations and platforms:'
repository: opencv/opencv
label: Concurrency
language: C++
comments_count: 4
repository_stars: 82865
---

When implementing concurrent code, always use the framework's provided synchronization primitives rather than direct language features. This ensures compatibility across all build configurations and platforms:

1. Use OpenCV synchronization mechanisms like `cv::getInitializationMutex()` and `cv::AutoLock` instead of standard C++ constructs like `std::mutex` and `std::lock_guard`:

```cpp
// Instead of this:
static std::mutex mtx;
std::lock_guard<std::mutex> lock(mtx);

// Use this:
cv::AutoLock lock(cv::getInitializationMutex());
```

2. Respect system threading settings with `cv::getNumThreads()` rather than hardcoding thread counts:

```cpp
// Instead of this:
m_parallel_runner = JxlThreadParallelRunnerMake(nullptr, 8); // Hardcoded value

// Use this:
m_parallel_runner = JxlThreadParallelRunnerMake(nullptr, cv::getNumThreads());
```

3. Be aware that thread counts vary by platform (e.g., Android defaults to 2, Linux uses all cores) and that nested parallel operations may be serialized.

4. When using static resources in multithreaded contexts, ensure proper synchronization or consider alternatives like on-demand initialization that avoid static state altogether.

These practices ensure your code remains compatible with special configurations like `OPENCV_DISABLE_THREAD_SUPPORT` while maintaining optimal performance across various platforms.
