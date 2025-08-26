---
title: Optimize CI workflow syntax
description: Write cleaner and more maintainable CI/CD workflows by following established
  syntax patterns and best practices. Use GitHub Actions' built-in features like `working-directory`
  instead of manual directory changes, employ proper shell quoting and efficient commands,
  and prefer single-line commands when appropriate.
repository: tree-sitter/tree-sitter
label: CI/CD
language: Yaml
comments_count: 4
repository_stars: 21799
---

Write cleaner and more maintainable CI/CD workflows by following established syntax patterns and best practices. Use GitHub Actions' built-in features like `working-directory` instead of manual directory changes, employ proper shell quoting and efficient commands, and prefer single-line commands when appropriate.

Key practices:
- Use `working-directory` parameter instead of `cd` commands in run steps
- Apply proper shell quoting (`"$variable"`) and use efficient command alternatives (`tar -xz -C` instead of `--directory=`)
- Use safe directory creation with `mkdir -p` to handle existing directories gracefully  
- Simplify single-line environment variable assignments instead of multi-line run blocks

Example improvements:
```yaml
# Instead of:
- name: Build WASM Library
  run: |
    cd lib/binding_web
    npm ci
    npm run build:debug

# Use:
- name: Build WASM Library
  working-directory: lib/binding_web
  run: npm ci && npm run build:debug

# Instead of:
- run: |
    echo "DOCKER_CMD=docker run --rm -v /home/runner:/home/runner -w . $CROSS_IMAGE" >> $GITHUB_ENV

# Use:
- run: echo "DOCKER_CMD=docker run --rm -v /home/runner:/home/runner -w . $CROSS_IMAGE" >> $GITHUB_ENV
```

These optimizations improve readability, reduce potential errors, and make workflows more maintainable while following GitHub Actions conventions.