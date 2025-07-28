---
title: Dynamic configuration handling
description: 'When implementing configuration changes that need to be applied at runtime,
  follow these practices:


  1. **Use reload mechanisms instead of immediate handling**: Don''t process configuration
  changes directly in dispatch functions. Instead, trigger reloads through proper
  channels.'
repository: hyprwm/Hyprland
label: Configurations
language: C++
comments_count: 6
repository_stars: 28863
---

When implementing configuration changes that need to be applied at runtime, follow these practices:

1. **Use reload mechanisms instead of immediate handling**: Don't process configuration changes directly in dispatch functions. Instead, trigger reloads through proper channels.

```cpp
// Don't do this:
if (COMMAND.contains("monitorv2")) {
    g_pConfigManager->handleMonitorv2();
    g_pConfigManager->m_wantsMonitorReload = true;
}

// Do this instead:
g_pEventLoopManager->doLater([this] {
    g_pConfigManager->m_wantsMonitorReload = true;
});
```

2. **Use static pointers for dynamic configuration**: For configuration values that need to change via hyprctl, use static CConfigValue pointers rather than copying values, as this enables runtime updates.

```cpp
// For dynamic config that changes via hyprctl:
static auto PDISABLELOGS = CConfigValue<Hyprlang::INT>("debug:disable_logs");

// Not this (copies value once):
Debug::coloredLogs = std::any_cast<Hyprlang::INT>(m_pConfig->getConfigValue("debug:colored_stdout_logs"));
```

3. **Use existing parsing utilities**: Leverage `configStringToInt` and similar utilities for consistent configuration parsing instead of implementing custom parsing logic.

```cpp
// Use existing utility:
PANIM->second.internalEnabled = configStringToInt(ARGS[1]);

// Instead of custom parsing:
if (ARGS[1] == "on" || ARGS[1] == "true" || ARGS[1] == "1")
    PANIM->second.internalEnabled = true;
```

4. **Check configuration existence properly**: When determining if a user has set a configuration value, use the appropriate methods to check the `set` flag rather than implementing custom existence checking.

This approach ensures configuration changes are processed consistently, can be updated dynamically, and maintain proper state management throughout the application lifecycle.