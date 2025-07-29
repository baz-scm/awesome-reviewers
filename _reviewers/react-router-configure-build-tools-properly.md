---
title: configure build tools properly
description: Ensure build configurations use proper package.json exports fields and
  TypeScript settings to avoid hard-coded paths and module format inconsistencies.
  Build tools should be configured to handle module resolution and output formats
  correctly to prevent runtime issues.
repository: remix-run/react-router
label: CI/CD
language: JavaScript
comments_count: 2
repository_stars: 55270
---

Ensure build configurations use proper package.json exports fields and TypeScript settings to avoid hard-coded paths and module format inconsistencies. Build tools should be configured to handle module resolution and output formats correctly to prevent runtime issues.

Use package.json exports field instead of hard-coding file paths:
```javascript
// Instead of hard-coded paths
input: `${SOURCE_DIR}/index.ts`,

// Use multiple inputs with proper exports configuration
input: [`${SOURCE_DIR}/index.ts`, `${SOURCE_DIR}/install.ts`],
```

Configure TypeScript and Babel properly for consistent module formats:
```javascript
typescript({
  tsconfig: path.join(__dirname, "tsconfig.json"),
  exclude: ["__tests__"],
  noEmitOnError: !WATCH,
  noForceEmit: true, // Prevents incorrect CJS exports in ESM builds
}),
babel({
  babelHelpers: "bundled",
  exclude: /node_modules/,
  extensions: [".ts"],
  ...remixBabelConfig, // Use shared configuration
})
```

This prevents build-time issues that can cause deployment failures and ensures consistent module handling across different environments.