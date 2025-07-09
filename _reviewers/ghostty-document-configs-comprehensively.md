---
title: Document configs comprehensively
description: 'Configuration options must be documented comprehensively with:


  1. Clear, descriptive name using appropriate platform prefixes (e.g., ''gtk-'' for
  GTK-specific options)'
repository: ghostty-org/ghostty
label: Configurations
language: Other
comments_count: 6
repository_stars: 32864
---

Configuration options must be documented comprehensively with:

1. Clear, descriptive name using appropriate platform prefixes (e.g., 'gtk-' for GTK-specific options)
2. Detailed explanation of the option's purpose and effect
3. Default value and valid value ranges
4. Version compatibility information if relevant
5. Example usage and specific use cases when the option might be needed

Example of well-documented config:

```zig
/// Controls whether to disable GDK color management in GTK applications.
///
/// By default this is set to `false`, meaning color management is enabled.
/// You may want to enable this setting (set to `true`) if you experience:
/// - Incorrect or washed out colors in your terminal
/// - Color inconsistencies between GTK applications
/// - Performance issues related to color management
///
/// This is a workaround for known issues with GTK's color management implementation,
/// particularly affecting applications running under Wayland.
/// Fixed in GTK 4.15.6.
@"gtk-gdk-disable-color-mgmt": bool = false,
```

Poor documentation can lead to user confusion, support issues, and inconsistent usage. Clear documentation helps users understand when and how to use configuration options effectively.