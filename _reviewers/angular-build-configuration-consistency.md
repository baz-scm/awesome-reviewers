---
title: Build configuration consistency
description: Maintain consistent build and release configurations across the project
  by following established patterns and ensuring documentation accuracy. When implementing
  new build configurations or modifying existing ones, reference how similar components
  handle the same requirements to maintain uniformity.
repository: angular/angular
label: CI/CD
language: Markdown
comments_count: 3
repository_stars: 98611
---

Maintain consistent build and release configurations across the project by following established patterns and ensuring documentation accuracy. When implementing new build configurations or modifying existing ones, reference how similar components handle the same requirements to maintain uniformity.

For package distribution, follow the same inclusion/exclusion patterns as other packages in the monorepo. For build tooling, use standardized configurations and document version-specific requirements clearly. For release processes, prefer simpler, more reliable commands over complex multi-step operations.

Example of consistent release packaging:
```shell
# Prefer this simple approach
git archive HEAD -o ~/angular-source.zip

# Over complex multi-command approaches
rm -rf dist/ **/node_modules/ && zip -r ~/angular-source.zip * -x ".git/*" -x "node_modules/*"
```

This approach reduces the likelihood of configuration drift, makes troubleshooting easier, and ensures that build processes remain reliable and maintainable across different environments and team members.