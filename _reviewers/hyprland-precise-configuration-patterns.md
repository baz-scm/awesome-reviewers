---
title: Precise configuration patterns
description: Use precise file patterns and correct installation paths in CMake configuration
  to avoid unintended inclusions and ensure proper system integration. Overly broad
  patterns can consume unrelated files from subprojects, while incorrect paths can
  break package discovery.
repository: hyprwm/Hyprland
label: Configurations
language: Txt
comments_count: 4
repository_stars: 28863
---

Use precise file patterns and correct installation paths in CMake configuration to avoid unintended inclusions and ensure proper system integration. Overly broad patterns can consume unrelated files from subprojects, while incorrect paths can break package discovery.

Key practices:
- Scope file globbing patterns appropriately (e.g., `src/*.h*` instead of `*.h*`)
- Use standard CMake modules like `GNUInstallDirs` for installation paths
- Specify precise file patterns in install commands with exclusions when needed
- Validate installation destinations match expected system conventions

Example of precise pattern usage:
```cmake
# Bad - too broad, includes subprojects
file(GLOB_RECURSE HEADERS_HL CONFIGURE_DEPENDS "*.h*")

# Good - scoped to source directory
file(GLOB_RECURSE HEADERS_HL CONFIGURE_DEPENDS "src/*.h*")

# Good - precise pattern with exclusions
install(DIRECTORY protocols/ DESTINATION include/hyprland/protocols 
        FILES_MATCHING PATTERN "*.h")

# Good - using standard CMake variables
install(TARGETS Hyprland hyprctl DESTINATION ${CMAKE_INSTALL_BINDIR})
```

This prevents build system confusion, ensures clean installations, and maintains compatibility across different environments and package managers.