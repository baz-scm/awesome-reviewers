---
title: Optimize CI/CD workflows
description: 'Configure CI/CD workflows to maximize efficiency and improve developer
  experience. Consider these key optimization practices:


  1. **Schedule automated jobs strategically**: Use offset minutes in cron schedules
  to avoid GitHub Actions high load times.'
repository: opentofu/opentofu
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 25901
---

Configure CI/CD workflows to maximize efficiency and improve developer experience. Consider these key optimization practices:

1. **Schedule automated jobs strategically**: Use offset minutes in cron schedules to avoid GitHub Actions high load times.
```yaml
# Schedule during off-peak hours with offset minutes to prevent queuing delays
schedule:
  - cron: '42 3 * * SUN'  # Using 42 instead of 0 reduces risk of delays
```

2. **Configure path exclusions**: Skip workflow runs for documentation and non-code changes to save CI resources.
```yaml
paths-ignore:
  - 'website/**'
  - 'docs/**'
```

3. **Progressive code quality enforcement**: Configure linters and code quality tools to only fail on new issues rather than existing ones, preventing contributors from being blocked by legacy problems.
```yaml
- name: golangci-lint
  uses: golangci/golangci-lint-action@v3
  with:
    version: v1.54
    only-new-issues: true  # Only enforce on changed code
```

These practices help maintain code quality while keeping CI/CD processes efficient and developer-friendly, ensuring the focus remains on new changes rather than fixing preexisting issues all at once.