---
title: Manage dependencies wisely
description: 'When configuring dependencies in composer.json files, follow these guidelines
  to ensure maintainable and reliable configurations:


  1. **Only include direct dependencies**: Add dependencies only when they are directly
  used by your package. If a dependency is accessed through another package, don''t
  include it directly.'
repository: laravel/framework
label: Configurations
language: Json
comments_count: 5
repository_stars: 33763
---

When configuring dependencies in composer.json files, follow these guidelines to ensure maintainable and reliable configurations:

1. **Only include direct dependencies**: Add dependencies only when they are directly used by your package. If a dependency is accessed through another package, don't include it directly.

```json
// AVOID - including unused direct dependencies
{
    "require": {
        "illuminate/contracts": "^12.0",
        "psr/simple-cache": "^1.0|^2.0|^3.0"  // Already included via illuminate/contracts
    }
}

// BETTER - only include what you directly use
{
    "require": {
        "illuminate/contracts": "^12.0"
    }
}
```

2. **Use appropriate dependency categories**: Place non-essential extensions and packages in the "suggest" section rather than "require" when they're only needed for optional features.

```json
// BETTER - use suggest for optional dependencies
{
    "require": {
        "php": "^8.2"
    },
    "suggest": {
        "ext-zlib": "For compression features",
        "spatie/fork": "For alternative concurrency driver"
    }
}
```

3. **Evaluate maintainer activity**: Before adding third-party dependencies, consider the package's maintenance status. For critical functionality, prefer actively maintained packages or consider implementing the functionality internally if maintenance is questionable.

4. **Use proper version constraints**: Format version constraints consistently and appropriately (use pipe | without spaces) and ensure they're compatible with all other dependencies.

```json
// AVOID
"laravel/serializable-closure": "^2.0@dev",
"laravel/prompts": "^0.1.20 || ^0.2 || ^0.3"

// BETTER
"laravel/serializable-closure": "^1.3|^2.0",
"laravel/prompts": "^0.1.20|^0.2|^0.3"
```

Following these practices helps maintain reliable, clearly defined configuration files that minimize surprises during updates and installations.
