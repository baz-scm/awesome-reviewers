---
title: Centralize configuration management
description: Prefer centralized configuration files (settings.json, settings.ts) over
  environment variables for application settings, especially when organizational control
  is needed. Avoid hardcoded assumptions about user environments and ensure configuration
  is loaded at appropriate initialization points.
repository: google-gemini/gemini-cli
label: Configurations
language: TSX
comments_count: 4
repository_stars: 65062
---

Prefer centralized configuration files (settings.json, settings.ts) over environment variables for application settings, especially when organizational control is needed. Avoid hardcoded assumptions about user environments and ensure configuration is loaded at appropriate initialization points.

Environment variables should be reserved for deployment-specific concerns, while user preferences and feature toggles belong in structured configuration files that support organizational policies and are easier to manage across multiple sources.

Example of preferred approach:
```typescript
// Instead of:
if (process.env.GEMINI_CLI_DISABLE_AUTOUPDATER === 'true') {
  return;
}

// Prefer:
if (settings.merged.disableAutoUpdater) {
  return;
}

// Load configuration early in initialization:
// Load custom themes from settings
themeManager.loadCustomThemes(settings.merged.customThemes);
```

This approach enables organizational control through settings.json files, reduces the complexity of merging configuration from multiple sources, and makes configuration more discoverable and maintainable. Additionally, organize reusable configuration interfaces in dedicated files rather than embedding them in component files to support future extensibility and reuse across the application.