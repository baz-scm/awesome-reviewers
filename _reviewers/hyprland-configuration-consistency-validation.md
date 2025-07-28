---
title: configuration consistency validation
description: When modifying configuration options, ensure changes are consistently
  applied across all relevant locations including default configuration files, documentation,
  example configs, and related codebases. Configuration inconsistencies create user
  confusion and maintenance burden.
repository: hyprwm/Hyprland
label: Configurations
language: Other
comments_count: 3
repository_stars: 28863
---

When modifying configuration options, ensure changes are consistently applied across all relevant locations including default configuration files, documentation, example configs, and related codebases. Configuration inconsistencies create user confusion and maintenance burden.

This reviewer addresses the common issue where developers update configuration in one location but forget to synchronize changes elsewhere. For example, when updating brightness control settings, the change must be reflected in both the main config and the default config header file.

Example of proper consistency:
```cpp
// In defaultConfig.hpp
bindel = ,XF86MonBrightnessUp, exec, brightnessctl -e4 -n2 set 5%+

// In example/hyprland.conf  
bindel = ,XF86MonBrightnessUp, exec, brightnessctl -e4 -n2 set 5%+
```

Before merging configuration changes, verify:
- Default configuration files are updated
- Example configurations reflect the changes  
- Documentation and wiki entries are synchronized
- Related configuration files use consistent syntax and values
- Environment variables are set in appropriate locations rather than duplicated

This practice prevents user confusion from conflicting examples and reduces maintenance overhead from scattered, inconsistent configuration references.