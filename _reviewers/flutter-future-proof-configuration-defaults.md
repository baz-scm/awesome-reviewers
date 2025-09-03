---
title: Future-proof configuration defaults
description: When designing configuration options, avoid hardcoded values and ensure
  defaults can be changed in future versions without breaking existing code. Make
  boolean flags negatable so users can opt out when defaults change, avoid ambiguous
  null vs empty configuration states, and provide clear migration paths for deprecated
  options.
repository: flutter/flutter
label: Configurations
language: Other
comments_count: 4
repository_stars: 172252
---

When designing configuration options, avoid hardcoded values and ensure defaults can be changed in future versions without breaking existing code. Make boolean flags negatable so users can opt out when defaults change, avoid ambiguous null vs empty configuration states, and provide clear migration paths for deprecated options.

Key practices:
- Make boolean flags negatable even if currently only one direction is useful: `addFlag('enable-feature', negatable: true)` allows future default changes
- Avoid hardcoded opinionated values like min/max ranges - make them configurable properties instead
- Distinguish between null (not set) and empty (explicitly disabled) configuration states to avoid ambiguity
- When deprecating configuration options, provide clear messaging about alternatives and timeline for removal

Example of good configuration design:
```dart
// Good: Negatable flag allows future default changes
addFlag('enable-gradle-managed-install', negatable: true)

// Good: Configurable properties instead of hardcoded values  
class ProgressBarConfig {
  final double minValue;
  final double maxValue; 
  // Instead of hardcoded setAttribute('aria-valuemin', "0")
}

// Good: Clear distinction between states
if (config != null && config.enabled) {
  // Feature explicitly enabled
} else if (config != null && !config.enabled) {
  // Feature explicitly disabled  
} else {
  // Feature not configured, use default behavior
}
```

This approach ensures configuration systems remain flexible and maintainable as requirements evolve, while providing clear upgrade paths for users.