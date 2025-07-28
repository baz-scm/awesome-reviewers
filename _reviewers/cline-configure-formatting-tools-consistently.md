---
title: Configure formatting tools consistently
description: Properly configure development tools to maintain consistent code formatting
  across the entire codebase and development environments. This includes setting up
  formatter ignore files, git attributes, and other configuration files that ensure
  uniform code style regardless of developer setup or platform differences.
repository: cline/cline
label: Code Style
language: Other
comments_count: 2
repository_stars: 48299
---

Properly configure development tools to maintain consistent code formatting across the entire codebase and development environments. This includes setting up formatter ignore files, git attributes, and other configuration files that ensure uniform code style regardless of developer setup or platform differences.

Key areas to configure:
- **Formatter exclusions**: Use `.prettierignore` or similar files to exclude generated directories, build outputs, and third-party code from formatting
- **Line ending consistency**: Configure `.gitattributes` with `* text=auto eol=lf` to prevent platform-specific line ending issues
- **Build output directories**: Exclude directories like `out/`, `build/`, `dist/` from formatting tools

Example configuration:
```
# .prettierignore
evals/
docs/
out/

# .gitattributes  
* text=auto eol=lf
```

This approach prevents formatting inconsistencies that can cause unnecessary diff noise and ensures all team members work with the same code style standards, regardless of their local development environment.