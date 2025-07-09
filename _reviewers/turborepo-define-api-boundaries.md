---
title: Define API boundaries
description: Clearly specify what constitutes your public API contract to manage versioning
  expectations and documentation requirements. Distinguish between structured outputs
  intended for programmatic consumption versus human-readable outputs that may change
  without being considered breaking changes.
repository: vercel/turborepo
label: API
language: Other
comments_count: 4
repository_stars: 28115
---

Clearly specify what constitutes your public API contract to manage versioning expectations and documentation requirements. Distinguish between structured outputs intended for programmatic consumption versus human-readable outputs that may change without being considered breaking changes.

For CLI tools or libraries:
- Document which outputs follow semantic versioning guarantees
- Explicitly mark pre-stable APIs in documentation
- Be precise about response formats and headers in endpoint documentation

Example in package exports:
```json
{
  "exports": {
    // Public API with stability guarantees
    ".": "./src/public-api.ts",
    
    // Explicitly mark experimental features
    "./experimental": "./src/experimental-features.ts",
    
    // Internal APIs not covered by semver
    "./internal": null
  }
}
```

When documenting API endpoints, be specific about response headers and their purposes, such as `x-artifact-tag` for artifact download endpoints. For authentication endpoints, clearly document their scope and intended usage contexts.