---
title: Centralize configuration management
description: Avoid hardcoded or duplicated configuration values by centralizing them
  in a dedicated location. When configurations are needed across multiple components,
  extract the logic for accessing and applying them so it can be reused. This prevents
  inconsistencies when configurations change and makes the codebase more maintainable.
repository: ghostty-org/ghostty
label: Configurations
language: Swift
comments_count: 3
repository_stars: 32864
---

Avoid hardcoded or duplicated configuration values by centralizing them in a dedicated location. When configurations are needed across multiple components, extract the logic for accessing and applying them so it can be reused. This prevents inconsistencies when configurations change and makes the codebase more maintainable.

**Instead of this:**
```swift
private enum WindowConfig {
    static let defaultSize = CGSize(width: 800, height: 600)
}
```

**Do this:**
```swift
// In a centralized configuration file/class
struct WindowConfigManager {
    func getDefaultSize(from config: AppConfig) -> CGSize {
        // Extract from config or fallback to default
        return CGSize(
            width: config.windowWidth ?? 800,
            height: config.windowHeight ?? 600
        )
    }
}

// When using the configuration
let windowSize = windowConfigManager.getDefaultSize(from: appConfig)
```

This approach ensures configurations are managed consistently, prevents duplicate values across the codebase, and makes it easier to update configuration behavior in one place.