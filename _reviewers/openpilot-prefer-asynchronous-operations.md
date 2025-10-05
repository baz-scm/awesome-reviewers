---
title: Prefer asynchronous operations
description: Use asynchronous patterns to prevent blocking operations from degrading
  system performance, especially in UI contexts and real-time systems. Prefer higher-level
  async abstractions like std::future over manual thread management when possible,
  as they provide automatic thread management, better exception handling, and simpler
  code maintenance.
repository: commaai/openpilot
label: Concurrency
language: Other
comments_count: 4
repository_stars: 58214
---

Use asynchronous patterns to prevent blocking operations from degrading system performance, especially in UI contexts and real-time systems. Prefer higher-level async abstractions like std::future over manual thread management when possible, as they provide automatic thread management, better exception handling, and simpler code maintenance.

For UI operations, ensure any potentially blocking calls (even those taking 0.1s) are made asynchronous to maintain smooth frame rates. For system operations that may block due to external factors (like network timeouts or hardware buffer states), isolate them in separate threads to prevent cascading delays.

Example from brightness control:
```cpp
// Preferred: Using std::future for automatic thread management
if (!brightness_future.valid() || 
    brightness_future.wait_for(std::chrono::seconds(0)) == std::future_status::ready) {
    brightness_future = std::async(std::launch::async, Hardware::set_brightness, brightness);
}

// Avoid: Manual thread management requiring explicit cleanup and exception handling
if (!brightness_thread || !brightness_thread->joinable()) {
    brightness_thread = std::make_unique<std::thread>(wrapper_function, brightness);
}
```

When operations must remain in separate threads due to blocking behavior (such as hardware buffer management), document the reasoning clearly and implement appropriate error handling for synchronization failures.