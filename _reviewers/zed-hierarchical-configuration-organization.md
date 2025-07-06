---
title: Hierarchical configuration organization
description: Organize configuration settings hierarchically by grouping related settings
  under meaningful namespaces rather than creating numerous top-level settings. This
  improves maintainability, discoverability, and reduces configuration sprawl as your
  application grows.
repository: zed-industries/zed
label: Configurations
language: Json
comments_count: 3
repository_stars: 62119
---

Organize configuration settings hierarchically by grouping related settings under meaningful namespaces rather than creating numerous top-level settings. This improves maintainability, discoverability, and reduces configuration sprawl as your application grows.

When adding a new setting, consider:
1. Whether it belongs under an existing settings group
2. If similar settings should be grouped together in a new namespace
3. How the setting might evolve with additional related options in the future

For example, instead of:

```json
{
  "show_user_picture": true,
  "show_onboarding_banner": true,
  "show_status_bar": true
}
```

Prefer:

```json
{
  "titlebar": {
    "show_user_picture": true,
    "show_onboarding_banner": true
  },
  "status_bar": {
    "visible": true
  }
}
```

This approach keeps configuration maintainable as features expand and makes settings easier to locate and understand in context. It also facilitates future extensions without cluttering the root configuration space.