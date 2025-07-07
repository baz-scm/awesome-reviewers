---
title: Verify platform compatibility first
description: When writing networking code that interacts with platform-specific features,
  always check for the existence of platform-specific functions or resources before
  attempting to use them. This prevents runtime errors when your code runs in different
  environments (Windows, Linux, macOS, containers) that might have different capabilities
  or implementations.
repository: tensorflow/tensorflow
label: Networking
language: Shell
comments_count: 2
repository_stars: 190625
---

When writing networking code that interacts with platform-specific features, always check for the existence of platform-specific functions or resources before attempting to use them. This prevents runtime errors when your code runs in different environments (Windows, Linux, macOS, containers) that might have different capabilities or implementations.

For example, when detecting network environment properties:

```python
import platform

# Good practice - check if function exists before using
def get_network_platform_info():
    info = {}
    
    # Define platform functions that might provide network-related information
    platform_checks = [
        ("network_os", "system"),
        ("container_environment", "freedesktop_os_release"),
        ("virtual_machine", "mac_ver")
    ]
    
    # Only use functions that exist on the current platform
    for label, function_name in platform_checks:
        if hasattr(platform, function_name):
            function = getattr(platform, function_name)
            info[label] = function()
        else:
            info[label] = "N/A"
    
    return info
```

This approach ensures your networking code gracefully handles different platforms rather than failing with attribute errors when a particular function isn't available.