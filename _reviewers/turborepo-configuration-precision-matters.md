---
title: Configuration precision matters
description: 'Ensure configuration files are precise and stable to prevent unexpected
  build failures and runtime issues. This includes:


  1. **Use correct syntax in configuration files**'
repository: vercel/turborepo
label: Configurations
language: Json
comments_count: 4
repository_stars: 28115
---

Ensure configuration files are precise and stable to prevent unexpected build failures and runtime issues. This includes:

1. **Use correct syntax in configuration files**
   Validate JSON files for syntax errors like extra commas, which can cause cryptic error messages during builds.
   
   ```json
   // Incorrect
   {
     "$schema": "https://turborepo.com/schema.json",,
     "ui": "tui"
   }
   
   // Correct
   {
     "$schema": "https://turborepo.com/schema.json",
     "ui": "tui"
   }
   ```

2. **Specify exact versions for critical dependencies**
   Use exact versions instead of ranges (`^` or `~`) for dependencies when stability is critical, especially in test fixtures or shared packages.
   
   ```json
   // Less stable (allows minor updates)
   "dependencies": {
     "@types/d3-scale": "^4.0.2"
   }
   
   // More stable (locks exact version)
   "dependencies": {
     "@types/d3-scale": "4.0.2"
   }
   ```

3. **Explicitly specify package manager**
   Include the `packageManager` field in package.json to ensure consistent behavior across environments, especially when using version wildcards (`*`).
   
   ```json
   {
     "name": "monorepo",
     "packageManager": "pnpm@8.14.0",
     "dependencies": {
       "util": "*"
     }
   }
   ```

4. **Establish clear sources of truth**
   Define which configuration files are authoritative for specific settings. For example, make package.json's `engines` field the definitive source for Node.js version requirements.
   
   ```json
   "engines": {
     "node": "22.x"
   }
   ```

These practices reduce configuration drift, prevent unexpected behavior, and help maintain consistency across environments and team members.