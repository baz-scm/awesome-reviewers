---
title: conditional feature initialization
description: Only initialize configuration-dependent features, systems, or resources
  when the relevant settings, flags, or conditions are actually present or enabled.
  This prevents unnecessary resource allocation, avoids unwanted side effects like
  creating default contexts, and improves performance by deferring expensive operations
  until they're needed.
repository: electron/electron
label: Configurations
language: Other
comments_count: 9
repository_stars: 117644
---

Only initialize configuration-dependent features, systems, or resources when the relevant settings, flags, or conditions are actually present or enabled. This prevents unnecessary resource allocation, avoids unwanted side effects like creating default contexts, and improves performance by deferring expensive operations until they're needed.

Key patterns to follow:
- Check for required configuration values before initializing dependent systems
- Use guard conditions to prevent initialization when features are disabled
- Wrap feature-specific code with appropriate build flags
- Defer expensive setup operations until the feature is actually used

Example of proper conditional initialization:
```cpp
// Bad: Always initializes prefs regardless of need
if (auto* browser_context = GetDefaultBrowserContext())
  prefs_ = browser_context->prefs();

// Good: Only initialize when actually needed
if (gin_helper::Dictionary restore_options;
    options.Get(options::kWindowStateRestoreOptions, &restore_options)) {
  // Only get prefs when stateId is present
  restore_options.Get(options::kStateId, &window_state_id_);
  if (!window_state_id_.empty()) {
    prefs_ = GetApplicationPrefs();
  }
}
```

Example with feature flags:
```cpp
// Wrap feature-specific code with build flags
#if BUILDFLAG(ENABLE_ELECTRON_EXTENSIONS)
  if (offscreen_use_shared_texture_) {
    dict.Set("texture", tex);
  }
#endif
```

This approach prevents creating unnecessary contexts, avoids performance overhead, and ensures features are only configured when they will actually be used.