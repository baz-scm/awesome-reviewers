---
title: Document configuration constraints clearly
description: When defining configuration options, always clearly document parameter
  constraints, valid ranges, and behaviors. For numeric values, explicitly state acceptable
  ranges and how out-of-range values are handled. Configuration options should have
  appropriate granularity - avoid simple booleans when more nuanced control is beneficial.
repository: zed-industries/zed
label: Configurations
language: Markdown
comments_count: 5
repository_stars: 62119
---

When defining configuration options, always clearly document parameter constraints, valid ranges, and behaviors. For numeric values, explicitly state acceptable ranges and how out-of-range values are handled. Configuration options should have appropriate granularity - avoid simple booleans when more nuanced control is beneficial.

For example, instead of:
```json
{
  "diagnostics": {
    "include_warnings": true
  }
}
```

Consider more granular control:
```json
{
  "diagnostics": {
    "minimum_level": "warning",  // Options: "error", "warning", "info", "hint"
    "inline": {
      "enabled": true
    }
  }
}
```

Group related settings logically, provide sensible defaults, and ensure configuration structure reflects the natural workflow (prerequisites before implementation details). This makes configurations more intuitive, flexible, and less prone to user error.