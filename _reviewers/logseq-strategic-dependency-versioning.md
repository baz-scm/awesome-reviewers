---
title: Strategic dependency versioning
description: Use strategic versioning approaches for dependencies based on their impact
  and maintenance status. Pin exact versions for dependencies that inject global styles,
  configurations, or behaviors to prevent unintended breaking changes during automatic
  updates. For unmaintained dependencies, evaluate alternatives or consider forking
  if there are useful pending...
repository: logseq/logseq
label: Configurations
language: Json
comments_count: 2
repository_stars: 37695
---

Use strategic versioning approaches for dependencies based on their impact and maintenance status. Pin exact versions for dependencies that inject global styles, configurations, or behaviors to prevent unintended breaking changes during automatic updates. For unmaintained dependencies, evaluate alternatives or consider forking if there are useful pending PRs that benefit your project.

Example from package.json:
```json
{
  "dependencies": {
    // Pin exact versions for global-affecting dependencies
    "@tailwindcss/forms": "0.5.3",
    "@tailwindcss/typography": "0.5.7",
    
    // Use semantic versioning for stable, well-maintained packages
    "@playwright/test": "^1.24.2",
    
    // Consider forking or alternatives for stale dependencies
    "remove-accents": "0.4.2" // Last updated 4 years ago - evaluate alternatives
  }
}
```

This approach balances stability with maintainability, ensuring that configuration changes are intentional while avoiding technical debt from abandoned dependencies.