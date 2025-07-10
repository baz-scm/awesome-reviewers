---
title: Descriptive identifier naming
description: Choose meaningful, self-explanatory names for variables, parameters,
  properties, and methods that clearly convey their purpose. Avoid abbreviations and
  acronyms unless they're widely understood industry standards.
repository: getsentry/sentry-php
label: Naming Conventions
language: PHP
comments_count: 9
repository_stars: 1873
---

Choose meaningful, self-explanatory names for variables, parameters, properties, and methods that clearly convey their purpose. Avoid abbreviations and acronyms unless they're widely understood industry standards.

For boolean variables, use prefixes like `is`, `has`, or `should` to improve readability:

```php
// Better
private $isFrozen = false;

// Instead of
private $frozen = false;
```

Use full descriptive names rather than acronyms or abbreviations for domain-specific concepts:

```php
// Better - reduces cognitive load for readers
$samplingContext = DynamicSamplingContext::fromTransaction($this->transaction);

// Instead of
$dsc = DynamicSamplingContext::fromTransaction($this->transaction);
```

Maintain consistency in parameter naming across related methods and classes:

```php
// Better - consistent naming pattern
public function fromArray(array $data): self
public function sanitizeData(array $data): array

// Instead of mixing naming styles
public function fromArray(array $array): self
public function sanitizeTags(array $tags): array
```

When naming test data variables, choose names that clearly describe what they represent rather than their type:

```php
// Better
public function testToArrayWithMessage(array $messageArguments, $expectedValue)

// Instead of
public function testToArrayWithMessage(array $message, $expectedValue)
```