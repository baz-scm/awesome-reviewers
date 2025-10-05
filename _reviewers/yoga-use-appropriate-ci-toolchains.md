---
title: Use appropriate CI toolchains
description: Ensure CI/CD workflows use technology-specific setup actions and execute
  commands in the correct working directories. Avoid using generic or unrelated setup
  actions that install unnecessary toolchains, as this increases build time and complexity.
  Always specify the appropriate working directory for technology-specific commands
  to ensure they execute in the...
repository: facebook/yoga
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 18255
---

Ensure CI/CD workflows use technology-specific setup actions and execute commands in the correct working directories. Avoid using generic or unrelated setup actions that install unnecessary toolchains, as this increases build time and complexity. Always specify the appropriate working directory for technology-specific commands to ensure they execute in the correct context.

For example, replace generic setup actions with technology-specific ones:
```yaml
# Instead of using setup-js for C# builds
- name: Setup
  uses: ./.github/actions/setup-js

# Use C#-specific setup
- name: Setup
  uses: ./.github/actions/setup-cs
```

And ensure commands run in the correct directory:
```yaml
- name: Restore Workloads
  run: dotnet workload restore
  working-directory: csharp
```

This practice improves build reliability, reduces unnecessary dependencies, and makes CI configuration more maintainable and understandable.