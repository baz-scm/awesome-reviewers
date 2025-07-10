---
title: Keep testing dependencies current
description: 'Regularly update testing framework dependencies (PHPUnit, PHPStan, etc.)
  to maintain compatibility with your project''s PHP version requirements and ensure
  access to new testing features. When updating dependencies, consider future compatibility
  needs by using appropriate version constraints. '
repository: getsentry/sentry-php
label: Testing
language: Json
comments_count: 2
repository_stars: 1873
---

Regularly update testing framework dependencies (PHPUnit, PHPStan, etc.) to maintain compatibility with your project's PHP version requirements and ensure access to new testing features. When updating dependencies, consider future compatibility needs by using appropriate version constraints. 

For critical testing tools like PHPUnit, evaluate whether version constraints should allow for newer major versions to support upcoming PHP versions (e.g., "^8.5" vs "^8.5|^9.0").

Example in composer.json:
```json
{
    "require-dev": {
        "phpunit/phpunit": "^8.5|^9.0", // Allows for PHP 8 testing in the future
        "symfony/phpunit-bridge": "^4.3",
        "phpstan/phpstan": "^0.11",
        "phpstan/phpstan-phpunit": "^0.11"
    }
}
```

Maintaining current testing dependencies helps prevent technical debt and ensures your test suite remains reliable as the project evolves.