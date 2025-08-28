---
title: Configuration bounds validation
description: Always validate configuration values against system limits and constraints,
  implementing automatic adjustment when values exceed acceptable bounds. This prevents
  runtime errors and ensures configurations remain within operational parameters.
repository: kilo-org/kilocode
label: Configurations
language: TSX
comments_count: 2
repository_stars: 7302
---

Always validate configuration values against system limits and constraints, implementing automatic adjustment when values exceed acceptable bounds. This prevents runtime errors and ensures configurations remain within operational parameters.

When setting configuration values that have system-imposed limits (like token counts, memory limits, or API constraints), implement validation logic that checks against maximum allowed values and automatically adjusts when necessary. For user-facing configuration displays, ensure accuracy by showing actual values rather than assumptions, and consider platform-specific variations.

Example implementation:
```typescript
// Validate and auto-adjust configuration values against system limits
useEffect(() => {
    if (isFeatureSupported && systemInfo?.maxLimit && userConfigValue > systemInfo.maxLimit) {
        setConfigurationField("configKey", systemInfo.maxLimit || DEFAULT_FALLBACK_VALUE)
    }
}, [isFeatureSupported, userConfigValue, systemInfo?.maxLimit, setConfigurationField])

// For display, show actual vs default values with platform awareness
const displayValue = userHasCustomized ? `${actualValue} [custom]` : `${defaultValue} [default]`
const platformKey = isMac ? "⌘" : "Ctrl"
```

This approach prevents configuration-related failures and provides users with accurate information about their current settings.