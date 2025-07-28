---
title: Use cross-platform commands
description: When writing CI/CD scripts and documentation, prefer Node.js APIs over
  shell commands for file operations to ensure cross-platform compatibility. Shell
  commands like `echo "content" > file` don't work consistently across different operating
  systems, particularly Windows, which can cause CI/CD pipelines to fail.
repository: prettier/prettier
label: CI/CD
language: Markdown
comments_count: 2
repository_stars: 50772
---

When writing CI/CD scripts and documentation, prefer Node.js APIs over shell commands for file operations to ensure cross-platform compatibility. Shell commands like `echo "content" > file` don't work consistently across different operating systems, particularly Windows, which can cause CI/CD pipelines to fail.

Instead of using shell-specific commands, use Node.js built-in APIs that work uniformly across all platforms:

```bash
# Avoid - doesn't work on Windows
echo "npx lint-staged" > .husky/pre-commit

# Prefer - works on all platforms
node --eval "fs.writeFileSync('.husky/pre-commit','npx lint-staged\n')"
```

This approach ensures that setup scripts, pre-commit hooks, and other CI/CD automation work reliably regardless of the operating system where they're executed, reducing platform-specific failures and improving the developer experience across diverse development environments.