---
title: prefer settings over environment
description: Prefer settings.json over environment variables and CLI flags for user
  configuration options. Environment variables should be reserved for system-level
  configuration or cases where the setting must be available before settings.json
  is loaded. CLI flags should be used for options that users frequently change between
  invocations.
repository: google-gemini/gemini-cli
label: Configurations
language: TypeScript
comments_count: 4
repository_stars: 65062
---

Prefer settings.json over environment variables and CLI flags for user configuration options. Environment variables should be reserved for system-level configuration or cases where the setting must be available before settings.json is loaded. CLI flags should be used for options that users frequently change between invocations.

Settings.json provides better user experience because:
- Users can configure options persistently without modifying shell environment
- Settings can be project-specific or user-global
- Configuration is more discoverable and self-documenting
- Avoids conflicts with other tools that use the same environment variables

Example of migrating an environment variable to settings:
```typescript
// Before: checking environment variable directly
const maxDirs = parseInt(process.env.GEMINI_MEMORY_DISCOVERY_MAX_DIRS ?? '', 10) || 200;

// After: using settings.json
interface Settings {
  memoryDiscoveryMaxDirs?: number;
}

// In code:
const maxDirs = settings.memoryDiscoveryMaxDirs ?? 200;
```

Reserve CLI flags for options that users need to change frequently (like `--model` for testing different models) and environment variables for system-level configuration that must be available during early initialization.