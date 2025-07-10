---
title: Use direct path imports
description: For optimal performance, use direct path imports instead of barrel imports
  when working with UI component libraries like Material UI. This practice improves
  both production bundle size through better tree-shaking and significantly enhances
  development server performance.
repository: mui/material-ui
label: Performance Optimization
language: Markdown
comments_count: 2
repository_stars: 96063
---

For optimal performance, use direct path imports instead of barrel imports when working with UI component libraries like Material UI. This practice improves both production bundle size through better tree-shaking and significantly enhances development server performance.

**Recommended:**
```javascript
// Good - Direct path import
import Button from '@mui/material/Button';
```

**Avoid:**
```javascript
// Avoid - Barrel import
import { Button } from '@mui/material';
```

While modern bundlers (Vite, Webpack 5+, Next.js 13.5+) handle tree-shaking well for production builds, barrel imports can severely slow down development server startup time and hot module reloading.

For enforcing this pattern across your team, consider configuring your editor to discourage barrel imports:

```json
// .vscode/settings.json
{
  "typescript.preferences.autoImportSpecifierExcludeRegexes": ["^@mui/[^\\/]+$"]
}
```

This small change can lead to significant performance improvements in large applications without requiring additional Babel plugins or complex configuration.