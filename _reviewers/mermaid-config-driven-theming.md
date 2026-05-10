---
title: Config-driven theming
description: 'When rendering/layout is affected by configuration or theming, avoid
  magic numbers and ad-hoc config handling. Instead:


  - Use a centralized “effective config” helper for all config-derived decisions,
  including correct type coercion (e.g., treat `"false"` the same as `false`).'
repository: mermaid-js/mermaid
label: Configurations
language: JavaScript
comments_count: 5
repository_stars: 87952
---

When rendering/layout is affected by configuration or theming, avoid magic numbers and ad-hoc config handling. Instead:

- Use a centralized “effective config” helper for all config-derived decisions, including correct type coercion (e.g., treat `"false"` the same as `false`).
- Derive theme-/appearance-sensitive values from `themeVariables` (or CSS vars like `--mermaid-font-family`) rather than hard-coding constants that break with different fonts/sizes.
- Apply theming values consistently across SVG/CSS/labels so users can rely on a single source of truth.
- If changing defaults would cause visual regressions, preserve existing behavior in the default path and gate improvements behind theme/config changes.

Example pattern:
```js
// config.js
export function getEffectiveFlowchartHtmlLabels(siteConfig) {
  // Correctly coerce string booleans
  const v = siteConfig?.flowchart?.htmlLabels;
  return v === true || v === 'true';
}
```
And for theme-derived styling:
```js
// instead of spacing = 60; or font-family: ${options.fontFamily};
const spacing = themeVariables?.noteSpacing ?? 60; // or derive from other theme vars
const fontFamily = 'var(--mermaid-font-family), trebuchet ms, verdana, arial, sans-serif';
```