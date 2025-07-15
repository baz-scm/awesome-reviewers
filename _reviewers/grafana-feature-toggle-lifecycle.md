---
title: Feature toggle lifecycle
description: 'When working with feature toggles and configuration flags, manage their
  entire lifecycle carefully to prevent breaking changes and compatibility issues. '
repository: grafana/grafana
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 68825
---

When working with feature toggles and configuration flags, manage their entire lifecycle carefully to prevent breaking changes and compatibility issues. 

Guidelines:
1. Document feature toggles when introduced, including purpose, scope, and expected removal timeline
2. Consider backward compatibility impacts before removing feature toggles
3. Ensure that configuration changes maintain compatibility with supported versions of dependent services
4. Provide migration paths when deprecating or removing configuration options

Example of proper feature toggle handling:

```typescript
// When introducing a feature toggle:
if (config.featureToggles.myNewFeature) {
  // New behavior with documentation
  // NOTE: This toggle supports X functionality and will be removed in version Y
  // when the feature becomes default behavior
}

// When maintaining backward compatibility:
if (config.featureToggles.legacyToggle || !options?.streamSelector) {
  return this.newBehavior(options);
} else {
  // Maintain compatibility with older versions
  const data = await this.legacyBehavior(options);
  return adaptToNewFormat(data);
}
```

Breaking changes to configuration defaults or removing feature toggles should be properly documented and typically done during major version updates, not in patch or minor releases.