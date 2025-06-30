---
title: Package.json configuration standards
description: 'Ensure package.json is correctly configured with proper module entry
  points and dependency categorization:


  1. **Module entry points**: Use the appropriate fields for different module systems
  to ensure compatibility across environments:'
repository: axios/axios
label: Configurations
language: Json
comments_count: 2
repository_stars: 107146
---

Ensure package.json is correctly configured with proper module entry points and dependency categorization:

1. **Module entry points**: Use the appropriate fields for different module systems to ensure compatibility across environments:
   ```json
   {
     "main": "dist/axios.js",     // CommonJS entry point
     "module": "index.js"         // ES modules entry point
   }
   ```

2. **Dependency categorization**: Place dependencies in the correct sections based on their usage:
   - `dependencies`: Runtime dependencies required for production
   - `devDependencies`: Development-only tools and libraries
   - `peerDependencies`: Compatible libraries that should be provided by the consuming application

   For polyfills and browser compatibility libraries like `whatwg-fetch`, consider whether they should be in `dependencies` rather than `devDependencies` if they're needed at runtime.

Proper configuration ensures consistent behavior across different environments and better dependency management.

## Discussions

