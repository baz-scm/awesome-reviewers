---
title: Platform-specific configuration separation
description: Configuration options should be separated between common/shared settings
  and platform-specific settings to avoid build failures and ensure proper cross-platform
  compatibility. When a configuration option is not supported on all target platforms
  or architectures, it must be moved from common configuration files to individual
  platform-specific configuration...
repository: zen-browser/desktop
label: Configurations
language: Other
comments_count: 2
repository_stars: 34711
---

Configuration options should be separated between common/shared settings and platform-specific settings to avoid build failures and ensure proper cross-platform compatibility. When a configuration option is not supported on all target platforms or architectures, it must be moved from common configuration files to individual platform-specific configuration files.

This separation prevents build failures that occur when unsupported options are included in common configurations. For example, DRM/Widevine support varies by architecture - Linux aarch64 doesn't support it while other platforms do.

Example of proper separation:
```
# configs/common/mozconfig - Remove platform-specific options
# ac_add_options --enable-eme=widevine  # REMOVED - not supported on all platforms

# configs/linux/mozconfig - Add for supported architectures only
if test "$ARCH" != "aarch64"; then
    ac_add_options --enable-eme=widevine
fi

# configs/macos/mozconfig - Add for supported platforms
ac_add_options --enable-eme=widevine
```

Before adding any configuration option to a common/shared configuration file, verify that it's supported across all target platforms and architectures. If not, place it in the appropriate platform-specific configuration files with proper conditional checks where needed.