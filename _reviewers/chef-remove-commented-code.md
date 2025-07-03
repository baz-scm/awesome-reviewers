---
title: Remove commented code
description: Avoid leaving commented-out code in the codebase. Version control systems
  already track the history of changes, making commented-out code unnecessary. Removing
  unused commented code improves readability, reduces confusion, and keeps the codebase
  clean.
repository: chef/chef
label: Code Style
language: Yaml
comments_count: 3
repository_stars: 7860
---

Avoid leaving commented-out code in the codebase. Version control systems already track the history of changes, making commented-out code unnecessary. Removing unused commented code improves readability, reduces confusion, and keeps the codebase clean.

Example of code to avoid:
```yaml
builder-to-testers-map:
  ubuntu-20.04-x86_64:
    - ubuntu-16.04-x86_64
    - ubuntu-18.04-x86_64
    - ubuntu-20.04-x86_64
  # windows-2012r2-i386:
  #   - windows-2012r2-i386
```

Instead, simply remove the commented lines completely. If the code needs to be referenced later, it can be found in the commit history.
