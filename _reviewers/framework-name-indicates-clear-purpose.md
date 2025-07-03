---
title: Name indicates clear purpose
description: Names should clearly indicate their purpose, type, and behavior. This
  applies to methods, variables, and parameters. Choose names that are self-documenting
  and unambiguous.
repository: laravel/framework
label: Naming Conventions
language: PHP
comments_count: 6
repository_stars: 33763
---

Names should clearly indicate their purpose, type, and behavior. This applies to methods, variables, and parameters. Choose names that are self-documenting and unambiguous.

Key guidelines:
- Use prefixes for boolean methods (is, has, can)
- Use accurate type indicators (integer vs number)
- Choose domain-specific terms (digits vs length for numbers)
- Avoid abbreviated or ambiguous names

Example:
```php
// Unclear naming
public function pan($value) { }
public function num($len = 6) { }

// Clear naming
public function formatPanNumber($value) { }
public function generateRandomInteger(int $digits = 6) { }

// Boolean method naming
public function arrayable($value) { }     // Unclear purpose
public function isArrayable($value) { }   // Clear purpose
```

This standard helps prevent confusion, makes code self-documenting, and maintains consistency across the codebase.
