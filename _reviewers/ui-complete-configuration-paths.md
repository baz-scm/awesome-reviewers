---
title: Complete configuration paths
description: Always verify that configuration files include all necessary file paths
  and extensions, particularly for framework-specific settings. Common issues include
  missing file extensions for TypeScript files, incorrect directory paths, and configurations
  that don't account for framework-specific directory structures.
repository: shadcn-ui/ui
label: Configurations
language: Other
comments_count: 3
repository_stars: 90568
---

Always verify that configuration files include all necessary file paths and extensions, particularly for framework-specific settings. Common issues include missing file extensions for TypeScript files, incorrect directory paths, and configurations that don't account for framework-specific directory structures.

When configuring Tailwind CSS with TypeScript support:
```js
module.exports = {
  content: [
    "./src/**/*.{html,js,jsx,tsx,ts}", // Include all relevant extensions
    "./app/**/*.{js,ts,jsx,tsx}", // For Next.js 13 app directory
    "./pages/**/*.{js,ts,jsx,tsx}", // For traditional Next.js pages
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  // Add comments to explain non-obvious configuration choices
  // ...
}
```

For framework-specific configurations like Laravel, double-check paths against the framework's expected directory structure (e.g., `resources/css/app.css` not `resources/app.css`). Adding comments to clarify framework-specific settings will help other developers understand your configuration choices, especially when supporting multiple versions or experimental features.