---
title: Purposeful documentation standards
description: Documentation should convey purpose and behavior, not just replicate
  code structure. Each docblock should explain what a component does and why it exists,
  rather than merely restating its name or signature.
repository: getsentry/sentry-php
label: Documentation
language: PHP
comments_count: 10
repository_stars: 1873
---

Documentation should convey purpose and behavior, not just replicate code structure. Each docblock should explain what a component does and why it exists, rather than merely restating its name or signature.

For classes and interfaces:
```php
/**
 * This class serves as a factory for HTTP clients, autodiscovering 
 * the HTTP client if none is passed by the user.
 */
final class HttpClientFactory implements HttpClientFactoryInterface
```

For methods and functions:
```php
/**
 * Gets the callbacks used to customize how objects are serialized 
 * in the payload of the event.
 * 
 * @return array<string, callable>
 */
public function getClassSerializers(): array
```

For getters/setters, avoid trivial descriptions like "Gets the X option" or "Sets the X option." Instead, explain the purpose:
```php
/**
 * Gets whether the silenced errors should be captured or not.
 * 
 * @return bool
 */
public function shouldCaptureSilencedErrors(): bool
```

When implementing interface methods, use the {@inheritdoc} tag while adding any additional context specific to the implementation:
```php
/**
 * {@inheritdoc}
 * 
 * This implementation uses PSR-7 compliant request objects.
 */
public function fetchRequest(): ?ServerRequestInterface
```

Empty docblocks or those that merely repeat the method name add no value and should be either enhanced with meaningful descriptions or removed entirely.