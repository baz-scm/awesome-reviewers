---
title: Build documentation clarity
description: Ensure build and deployment documentation clearly explains processes,
  outputs, and environment options to prevent CI/CD pipeline issues. Documentation
  should comprehensively cover build context separation, deployment targets, and generated
  artifacts.
repository: nuxt/nuxt
label: CI/CD
language: Markdown
comments_count: 3
repository_stars: 57769
---

Ensure build and deployment documentation clearly explains processes, outputs, and environment options to prevent CI/CD pipeline issues. Documentation should comprehensively cover build context separation, deployment targets, and generated artifacts.

When documenting build processes, include:
- Clear explanation of build outputs and their purposes (e.g., `index.html`, `200.html`, `404.html` for prerendering)
- Deployment environment options with specific examples
- Build vs runtime context separation to prevent configuration errors

Example:
```markdown
## Build Output
When prerendering a client-rendered app, Nuxt generates `index.html`, `200.html` and `404.html` files by default. You can deploy this output on any system supporting JavaScript, including serverless and edge environments, or pre-render for static hosting.

## Context Separation  
`nuxt.config` and Nuxt Modules extend the build context, whereas Nuxt Plugins extend runtime. These contexts are isolated and should not share state.
```

This prevents CI/CD pipeline failures caused by unclear build requirements, incorrect deployment configurations, or context mixing issues.