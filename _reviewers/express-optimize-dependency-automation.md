---
title: Optimize dependency automation
description: Configure automated dependency update tools (like Dependabot) to balance
  security needs against developer cognitive load. Set monthly intervals instead of
  weekly to reduce PR noise, limit the number of concurrent PRs, and consider excluding
  major version updates that could cause compatibility issues.
repository: expressjs/express
label: Configurations
language: Yaml
comments_count: 4
repository_stars: 67300
---

Configure automated dependency update tools (like Dependabot) to balance security needs against developer cognitive load. Set monthly intervals instead of weekly to reduce PR noise, limit the number of concurrent PRs, and consider excluding major version updates that could cause compatibility issues.

Example configuration for Dependabot:
```yaml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: monthly
      time: "23:00"
      timezone: Europe/London
    open-pull-requests-limit: 10
    ignore:
      - dependency-name: "*"
        update-types: ["version-update:semver-major"]
```

This configuration reduces PR noise with monthly updates, limits open PRs to 10, schedules updates during off-hours, and avoids major version updates that might break compatibility.