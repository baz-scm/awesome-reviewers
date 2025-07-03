---
title: Keep CI configurations minimal
description: 'When configuring CI workflows, include only the extensions, tools, and
  settings that are necessary for the specific tests being run. Avoid adding unnecessary
  PHP extensions (such as `xml` or `xdebug`) to workflow configurations unless they''re
  explicitly required. Similarly, keep coverage disabled (`coverage: none`) in CI
  pipelines by default to improve...'
repository: laravel/framework
label: CI/CD
language: Yaml
comments_count: 14
repository_stars: 33763
---

When configuring CI workflows, include only the extensions, tools, and settings that are necessary for the specific tests being run. Avoid adding unnecessary PHP extensions (such as `xml` or `xdebug`) to workflow configurations unless they're explicitly required. Similarly, keep coverage disabled (`coverage: none`) in CI pipelines by default to improve performance.

Example:
```yaml
- name: Setup PHP
  uses: shivammathur/setup-php@v2
  with:
    php-version: 8.3
    extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, pdo_mysql, :php-psr
    coverage: none
```

This approach keeps CI workflows efficient, reduces execution time, and avoids potential issues from unnecessary dependencies.
