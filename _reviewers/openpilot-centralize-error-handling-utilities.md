---
title: Centralize error handling utilities
description: Create reusable error handling functions that accept custom error callbacks
  instead of duplicating error handling logic across multiple files. This approach
  provides flexibility in error response while maintaining consistent error handling
  patterns throughout the codebase.
repository: commaai/openpilot
label: Error Handling
language: Other
comments_count: 2
repository_stars: 58214
---

Create reusable error handling functions that accept custom error callbacks instead of duplicating error handling logic across multiple files. This approach provides flexibility in error response while maintaining consistent error handling patterns throughout the codebase.

When implementing system calls or operations that can fail, use a centralized utility function that accepts an error message and a callback for custom error handling. This eliminates code duplication and allows each call site to define appropriate failure responses.

Example implementation:
```cpp
template<typename ErrorCallback>
int safe_ioctl(int fd, unsigned long request, void *argp, const char* error_msg, ErrorCallback error_callback) {
  int ret;
  do {
    ret = ioctl(fd, request, argp);
  } while ((ret == -1) && (errno == EINTR));

  if (ret == -1 && error_msg) {
    LOGE("ioctl failed: %s", error_msg);
    error_callback();
  }
  return ret;
}

// Usage with custom error handling
auto fail = [this, serial] {
  cleanup(); 
  throw std::runtime_error("Error connecting to panda " + serial);
};
safe_ioctl(spi_fd, SPI_IOC_WR_MODE, &spi_mode, "failed setting SPI mode", fail);
```

This pattern allows for consistent error logging while enabling call sites to implement appropriate cleanup, exception throwing, or recovery strategies based on their specific context.