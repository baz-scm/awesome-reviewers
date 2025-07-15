---
title: Explicit configuration specifications
description: 'When writing configuration files, be explicit and precise about dependencies
  and versions rather than using broad patterns or tags.


  For dependency declarations:'
repository: mui/material-ui
label: Configurations
language: TypeScript
comments_count: 4
repository_stars: 96063
---

When writing configuration files, be explicit and precise about dependencies and versions rather than using broad patterns or tags.

For dependency declarations:
- List specific dependencies rather than relying on wildcards when possible
- Document why certain dependencies need special handling
- Maintain comprehensive lists of dependencies that require special configuration

For version specifications:
- Use semantic versioning ranges (e.g., `^6.0.0`) instead of tags like `latest` or `latest-v6`
- Avoid single version identifiers when packages follow independent versioning

Example of good configuration practice:
```typescript
// In build config file
export default defineConfig({
  // Explicitly list dependencies with clear comments
  ssr: {
    // Specific comment explaining the need for these dependencies
    optimizeDeps: {
      include: ['@emotion/react', '@emotion/styled', '@mui/material', '@mui/icons-material'],
    },
    noExternal: ['@emotion/react', '@emotion/styled', '@mui/material', '@mui/icons-material'],
  },
  dependencies: {
    '@mui/material': '^6.0.0',  // Explicit version range instead of 'latest'
    'react': '^18.0.0',
    'react-dom': '^18.0.0',
  }
});
```

This approach improves maintenance, reproduceability of issues, and makes configuration requirements explicit rather than implicit.