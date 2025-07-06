---
title: Minimize workflow complexity
description: 'Keep GitHub Actions workflows efficient and maintainable by eliminating
  redundant configurations and ensuring comprehensive test coverage:


  1. **Avoid redundant environment variables** - Use the minimum number of variables
  needed to achieve your workflow goals. When one variable can be derived from another,
  don''t store both.'
repository: bridgecrewio/checkov
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 7668
---

Keep GitHub Actions workflows efficient and maintainable by eliminating redundant configurations and ensuring comprehensive test coverage:

1. **Avoid redundant environment variables** - Use the minimum number of variables needed to achieve your workflow goals. When one variable can be derived from another, don't store both.

Example refactoring:
```yaml
# Not recommended
- name: Filter files
  run: |
    YAML_JSON_FILES=$(echo ${{ steps.changed-files.outputs.all_changed_files }} | grep -E '\.ya?ml$|\.json$')
    echo "YAML_JSON_FILES=$YAML_JSON_FILES" >> "$GITHUB_ENV"
    echo "RELEVANT_FILES_CHANGED=true" >> "$GITHUB_ENV"

# Recommended
- name: Filter files
  run: |
    YAML_JSON_FILES=$(echo ${{ steps.changed-files.outputs.all_changed_files }} | grep -E '\.ya?ml$|\.json$')
    echo "YAML_JSON_FILES=$YAML_JSON_FILES" >> "$GITHUB_ENV"
    
- name: Next step
  if: env.YAML_JSON_FILES != ''
  # Use YAML_JSON_FILES directly instead of a redundant flag
```

2. **Define comprehensive test matrices** - Ensure matrix strategies include all relevant versions of languages, tools, or environments needed for thorough testing.

```yaml
# Not recommended
strategy:
  matrix:
    python: ["3.8"]  # Incomplete coverage

# Recommended
strategy:
  matrix:
    python: ["3.8", "3.9", "3.10", "3.11"]  # Complete coverage
```

Keeping workflows streamlined improves maintainability, reduces debugging time, and makes your CI processes more reliable.