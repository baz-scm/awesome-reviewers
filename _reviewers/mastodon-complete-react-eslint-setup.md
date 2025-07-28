---
title: complete React ESLint setup
description: When configuring ESLint for React projects, ensure you include comprehensive
  React-specific configurations beyond the basic setup. Include both the React import
  plugin configuration and JSX runtime configuration to get enhanced linting rules
  and automatic fixes.
repository: mastodon/mastodon
label: React
language: Other
comments_count: 2
repository_stars: 48691
---

When configuring ESLint for React projects, ensure you include comprehensive React-specific configurations beyond the basic setup. Include both the React import plugin configuration and JSX runtime configuration to get enhanced linting rules and automatic fixes.

Essential React ESLint configurations to include:
- `importPlugin.flatConfigs.react` for React-specific import rules
- `react.configs.flat["jsx-runtime"]` for automatic JSX configuration and fixes

Example configuration:
```javascript
extends: [
  js.configs.recommended,
  react.configs.flat.recommended,
  react.configs.flat["jsx-runtime"], // Auto-configures JSX handling
  reactHooks.configs['recommended-latest'],
  jsxA11Y.flatConfigs.recommended,
  importPlugin.flatConfigs.recommended,
  importPlugin.flatConfigs.react, // React-specific import rules
  // ... other configurations
],
```

These additional configurations provide automatic fixes for common React patterns and ensure comprehensive linting coverage for React-specific code patterns, imports, and JSX usage.