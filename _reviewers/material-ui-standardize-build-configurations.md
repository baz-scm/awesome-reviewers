---
title: Standardize build configurations
description: When configuring module builds, maintain consistent and explicit configuration
  for different module formats (CJS, ESM, modern) to ensure compatibility across environments.
  Package exports should be clearly defined with appropriate conditions for each module
  system.
repository: mui/material-ui
label: Configurations
language: Other
comments_count: 4
repository_stars: 96063
---

When configuring module builds, maintain consistent and explicit configuration for different module formats (CJS, ESM, modern) to ensure compatibility across environments. Package exports should be clearly defined with appropriate conditions for each module system.

Best practices:

1. Use explicit file extensions (.js, .mjs, .cjs) to avoid reliance on package.json lookups for determining module type:
```javascript
const packageExports = {
  '.': {
    types: './index.d.ts',
    import: './index.mjs',     // ESM with .mjs extension
    'mui-modern': './index.modern.mjs',  // Modern build with condition
    require: './index.js',     // CJS with .js extension
  },
  // Other exports...
};
```

2. Consider build output organization that supports multiple module formats while maintaining backward compatibility:
   - Either use separate directories (cjs/, esm/) for different formats
   - Or use a flat structure with distinct file extensions (.mjs, .cjs)

3. Ensure all necessary metadata (like sideEffects) is included in all package.json configurations

4. Document module resolution strategy and compatibility with different Node.js versions, especially when supporting legacy environments