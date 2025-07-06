---
title: Judicious configuration management
description: 'Carefully manage configuration options, including feature flags, to
  balance flexibility with maintainability:


  1. **Use feature flags strategically:**'
repository: grafana/grafana
label: Configurations
language: Go
comments_count: 4
repository_stars: 68825
---

Carefully manage configuration options, including feature flags, to balance flexibility with maintainability:

1. **Use feature flags strategically:**
   - Put new features behind feature flags for gradual rollout
   - Once fully deployed, remove the flag and make the feature standard
   - Avoid feature flags when default behavior naturally preserves backward compatibility

```go
// Good: Feature flag for gradual rollout
if featuremgmt.AnyEnabled(&featuremgmt.FeatureManager{}, featuremgmt.FlagNewFeature) {
    providers = []app.Provider{playlistAppProvider, shortURLAppProvider}
} else {
    providers = []app.Provider{playlistAppProvider}
}

// Better when possible: Backward compatible default behavior
options := getCookieOptions()
if featuremgmt.AnyEnabled(&featuremgmt.FeatureManager{}, featuremgmt.FlagPanelExporterCookieDomain) {
    // Only modify behavior when flag is enabled
} else {
    options.Domain = "" // Maintains previous behavior
}
```

2. **Limit configuration points:**
   - Start with fewer configuration options and add more only when needed
   - Remember that once a configuration option is exposed, removing it may break user workflows
   - Consider using appropriate metadata for feature flags (like `HideFromDocs: true` for internal features)

3. **Reuse existing configuration parsers** rather than creating new ones to ensure consistent behavior across the application.