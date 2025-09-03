---
title: Use configuration constants
description: Always use named constants, enums, or well-defined configuration objects
  instead of magic strings, numbers, or inline literals for configuration values.
  This improves maintainability, reduces typos, enables better IDE support, and makes
  configuration changes easier to track.
repository: menloresearch/jan
label: Configurations
language: TSX
comments_count: 4
repository_stars: 37620
---

Always use named constants, enums, or well-defined configuration objects instead of magic strings, numbers, or inline literals for configuration values. This improves maintainability, reduces typos, enables better IDE support, and makes configuration changes easier to track.

Examples of good practices:
- Use enums for status values: `status === EngineStatus.ready` instead of `status === 'ready'`
- Define constants for localStorage keys: `const EXPERIMENTAL_FEATURE = 'experimentalFeature'` instead of inline strings
- Use declarative configuration arrays with proper defaults: `localStorage.getItem(HTTPS_PROXY_FEATURE) ?? ""`
- Avoid optional parameters for configuration that always has a value: `serverEnabled: boolean` instead of `serverEnabled?: boolean`

This approach makes configuration management more robust and prevents runtime errors from typos in configuration keys or values.