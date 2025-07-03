---
title: Disable coverage in workflows
description: Keep code coverage tools disabled in CI/CD workflows unless they're specifically
  needed for generating coverage reports. Enabling coverage tools like xdebug in GitHub
  Actions can significantly slow down pipeline execution without providing value when
  reports aren't being collected or analyzed.
repository: laravel/framework
label: Testing
language: Yaml
comments_count: 4
repository_stars: 33763
---

Keep code coverage tools disabled in CI/CD workflows unless they're specifically needed for generating coverage reports. Enabling coverage tools like xdebug in GitHub Actions can significantly slow down pipeline execution without providing value when reports aren't being collected or analyzed.

When configuring PHP environments in workflows, explicitly set `coverage: none` and avoid including coverage extensions like xdebug unless they serve a specific purpose:

```yaml
uses: shivammathur/setup-php@v2
with:
  php-version: 8.2
  extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, pdo_mysql, :php-psr
  tools: composer:v2
  coverage: none  # Keep coverage disabled for better performance
```

Reserve coverage tools for dedicated testing jobs that specifically generate and process coverage reports. This helps maintain faster CI pipelines while still allowing coverage analysis when needed.
