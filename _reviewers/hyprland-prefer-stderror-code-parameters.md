---
title: prefer std::error_code parameters
description: When using std::filesystem operations, prefer passing std::error_code
  parameters instead of relying on try-catch blocks for error handling. This approach
  provides better performance and more explicit error checking.
repository: hyprwm/Hyprland
label: Error Handling
language: C++
comments_count: 4
repository_stars: 28863
---

When using std::filesystem operations, prefer passing std::error_code parameters instead of relying on try-catch blocks for error handling. This approach provides better performance and more explicit error checking.

Most std::filesystem functions have overloads that accept an std::error_code reference parameter. Use these overloads and check the error code explicitly rather than catching exceptions.

Example:
```cpp
// Avoid try-catch approach
try {
    if (std::filesystem::exists(path) && std::filesystem::is_directory(path)) {
        // process directory
    }
} catch (...) {
    // handle error
}

// Prefer error_code approach
std::error_code ec1, ec2;
if (std::filesystem::exists(path, ec1) && !ec1 && 
    std::filesystem::is_directory(path, ec2) && !ec2) {
    // process directory
} else if (ec1 || ec2) {
    // handle specific errors
}
```

This pattern is especially important for operations like `std::filesystem::exists()`, `std::filesystem::is_directory()`, `std::filesystem::canonical()`, and directory iteration where exceptions can be thrown for various system-level issues. The error_code approach allows for more granular error handling and avoids the performance overhead of exception handling in expected error scenarios.