---
title: Verify configuration documentation
description: Ensure that all configuration documentation accurately reflects the actual
  implementation, especially for build tools, tech stack, and architectural decisions.
  When documenting configurations that deviate from standard practices, provide clear
  rationale for the choices made.
repository: lobehub/lobe-chat
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 65138
---

Ensure that all configuration documentation accurately reflects the actual implementation, especially for build tools, tech stack, and architectural decisions. When documenting configurations that deviate from standard practices, provide clear rationale for the choices made.

Key areas to verify:
- Build tool configurations (development vs production environments)
- Tech stack accuracy (distinguish between direct usage vs internal dependencies)
- Architectural patterns and their justifications

Example from the codebase:
```markdown
# Incorrect documentation
- **Build Tools**: Turbo, Vite

# Corrected documentation  
- **Build Tools**: Turbo (monorepo), Turbopack (Next.js dev), Webpack (Next.js prod)
- **Testing**: Vitest (uses Vite internally, but Vite not used directly in main build)
```

For architectural decisions like using multiple stores instead of the recommended single store pattern, document the complexity-based rationale and provide guidance on when each approach should be used. This prevents confusion during development and helps new team members understand the reasoning behind configuration choices.