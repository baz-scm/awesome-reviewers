---
title: Explicit CI configurations
description: CI/CD workflows should use explicit, named configurations rather than
  wildcards, globs, or implicit behaviors to improve maintainability and debuggability.
  This makes it easier for developers to understand failures and reduces silent errors.
repository: duckdb/duckdb
label: CI/CD
language: Yaml
comments_count: 6
repository_stars: 32061
---

CI/CD workflows should use explicit, named configurations rather than wildcards, globs, or implicit behaviors to improve maintainability and debuggability. This makes it easier for developers to understand failures and reduces silent errors.

Key practices:
- Use explicit job names and dependencies instead of wildcards (e.g., individual config files with logical names like "encrypted_db.config" rather than globbing "test/configs/*")
- Specify exact build targets instead of pattern matching (e.g., "cp310" instead of "cp310-*")
- Add proper job dependencies with `needs:` to ensure correct execution order
- Use explicit file handling that fails on missing files rather than silently continuing
- Maintain lean, explicit version matrices with only necessary combinations

Example of explicit vs implicit configuration:
```yaml
# Avoid: Implicit glob pattern
run: |
  for file in test/configs/*; do
    ./build/release/test/unittest --test-config "$file"
  done

# Prefer: Explicit named jobs
encrypted-db-test:
  name: Encrypted Database Test
  run: ./build/release/test/unittest --test-config encrypted_db.config

performance-test:
  name: Performance Test  
  run: ./build/release/test/unittest --test-config performance.config
```

This approach makes CI failures easier to diagnose and workflows more maintainable for the development team.