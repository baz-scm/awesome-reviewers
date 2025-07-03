---
title: Platform-agnostic network APIs
description: When implementing networking functionality, ensure code uses platform-agnostic
  APIs and appropriate abstraction layers to handle differences between Windows, Unix,
  and macOS systems. Similar to how string operations require platform-specific handling
  (as seen in discussion 1 where `strchr` was replaced with `app_candidate.find(DIR_SEPARATOR)`),
  networking...
repository: dotnet/runtime
label: Networking
language: C++
comments_count: 3
repository_stars: 16578
---

When implementing networking functionality, ensure code uses platform-agnostic APIs and appropriate abstraction layers to handle differences between Windows, Unix, and macOS systems. Similar to how string operations require platform-specific handling (as seen in discussion 1 where `strchr` was replaced with `app_candidate.find(DIR_SEPARATOR)`), networking code should avoid direct OS-specific socket APIs in favor of cross-platform abstractions.

Example:
```cpp
// Avoid platform-specific code like this:
#ifdef _MSC_VER
    SOCKET sock = socket(AF_INET, SOCK_STREAM, 0);
    // Windows-specific socket operations
#else
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    // Unix-specific socket operations
#endif

// Instead, use platform abstraction layers:
pal::socket_t sock = pal::create_socket(pal::AddressFamily::IPv4, pal::SocketType::Stream);
if (pal::connect_socket(sock, address, port))
{
    // Platform-agnostic socket operations
}
```

This approach ensures consistent behavior across all supported platforms and simplifies maintenance by centralizing platform-specific code in the abstraction layer.
