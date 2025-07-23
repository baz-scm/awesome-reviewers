---
title: Configuration naming conventions
description: 'When adding new configuration settings, follow these naming conventions
  to maintain consistency and clarity:


  1. **For related components**: Use a unified setting with resource scope instead
  of creating duplicate settings. For example, instead of having separate `typescript.maximumHoverLength`
  and `javascript.maximumHoverLength` settings, create a single...'
repository: microsoft/vscode
label: Configurations
language: Json
comments_count: 2
repository_stars: 174887
---

When adding new configuration settings, follow these naming conventions to maintain consistency and clarity:

1. **For related components**: Use a unified setting with resource scope instead of creating duplicate settings. For example, instead of having separate `typescript.maximumHoverLength` and `javascript.maximumHoverLength` settings, create a single `js/ts.hover.maximumLength` with resource scope:

```json
"js/ts.hover.maximumLength": {
  "type": "number",
  "default": 500,
  "description": "Controls the maximum length of hover content",
  "scope": "resource"
}
```

This approach allows for language-specific configuration while reducing configuration sprawl.

2. **For experimental features**: Clearly mark experimental settings in both their naming and metadata:
   - Prefix the setting name with `experimental` (e.g., `typescript.experimental.useTsgo` instead of `typescript.useTsgo`)
   - Include the "experimental" tag in the configuration metadata:

```json
"typescript.experimental.useTsgo": {
  "type": "boolean",
  "default": false,
  "description": "Controls whether to use TsGo for TypeScript processing",
  "tags": ["experimental"]
}
```

These conventions improve discoverability, communicate the stability status of features, and help maintain a cleaner configuration surface for users.