---
title: Package manager consistency
description: Maintain consistent package manager usage throughout the project lifecycle.
  When a project uses yarn (indicated by yarn.lock), avoid committing npm's package-lock.json
  file, as having both lock files can cause dependency resolution conflicts and inconsistent
  builds across different environments.
repository: ChatGPTNextWeb/NextChat
label: Configurations
language: Json
comments_count: 2
repository_stars: 85721
---

Maintain consistent package manager usage throughout the project lifecycle. When a project uses yarn (indicated by yarn.lock), avoid committing npm's package-lock.json file, as having both lock files can cause dependency resolution conflicts and inconsistent builds across different environments.

Key practices:
- Choose one package manager (npm or yarn) and stick with it
- Only commit the lock file corresponding to your chosen package manager
- Remove conflicting lock files from version control
- Ensure all team members use the same package manager

Example violation:
```
# Project structure showing both lock files (problematic)
├── package.json
├── yarn.lock          # Using yarn
└── package-lock.json  # Should not exist when using yarn
```

This practice ensures reproducible builds and prevents confusion about which package manager and dependency versions should be used in different environments.