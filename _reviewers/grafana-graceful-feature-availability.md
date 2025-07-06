---
title: Graceful feature availability
description: When implementing configurable features, ensure they degrade gracefully
  based on environment conditions like feature flags, plugin availability, or license
  status. Instead of showing disabled buttons or non-functional UI elements, provide
  informative feedback about why a feature is unavailable and how to enable it.
repository: grafana/grafana
label: Configurations
language: TSX
comments_count: 3
repository_stars: 68825
---

When implementing configurable features, ensure they degrade gracefully based on environment conditions like feature flags, plugin availability, or license status. Instead of showing disabled buttons or non-functional UI elements, provide informative feedback about why a feature is unavailable and how to enable it.

For feature flags:
```tsx
{config.featureToggles.myFeature && (
  <MyFeatureComponent />
)}
```

For optional dependencies:
```tsx
{!config.rendererAvailable ? (
  <Alert severity="info" title="Image renderer plugin not installed">
    <Trans i18nKey="feature-availability.renderer-instructions">
      To render images, you must install the{' '}
      <a href="..." target="_blank" rel="noopener noreferrer">
        Grafana image renderer plugin
      </a>
      . Please contact your administrator to install the plugin.
    </Trans>
  </Alert>
) : (
  <FeatureControls />
)}
```

For edition-specific features:
```tsx
{config.buildInfo.edition === GrafanaEdition.OpenSource && (
  <OpenSourceSpecificContent />
)}
```

This approach improves user experience by setting clear expectations about feature availability and providing guidance for enablement, rather than exposing UI elements that won't work in the current environment.