---
title: Flexible configuration formats
description: Support multiple configuration formats where appropriate (string, callable,
  object) to accommodate different frameworks and usage patterns. This improves developer
  experience across different ecosystems (like Laravel, Symfony) while maintaining
  type safety through proper validation.
repository: getsentry/sentry-php
label: Configurations
language: PHP
comments_count: 4
repository_stars: 1873
---

Support multiple configuration formats where appropriate (string, callable, object) to accommodate different frameworks and usage patterns. This improves developer experience across different ecosystems (like Laravel, Symfony) while maintaining type safety through proper validation.

For example, when implementing a configuration option that accepts a callback:

```php
/**
 * Gets a callback that will be invoked when we sample a Transaction.
 *
 * @psalm-return \Sentry\Tracing\TracesSamplerInterface|callable(\Sentry\Tracing\SamplingContext): float
 */
public function getTracesSampler()
{
    if (\is_string($this->options['traces_sampler']) && class_exists($this->options['traces_sampler'])) {
        return new $this->options['traces_sampler']();
    }

    return $this->options['traces_sampler'];
}
```

Ensure proper validation:

```php
// In configureOptions method:
$resolver->setAllowedTypes('traces_sampler', ['null', 'string', 'callable', 'object']);
```

For values that should be configurable across projects, extract them as options or constants rather than hardcoding them:

```php
// Instead of hardcoding:
$keysToRemove = ['authorization', 'cookie', 'set-cookie', 'remote_addr'];

// Extract to a constant:
private const HEADERS_TO_SANITIZE = ['authorization', 'cookie', 'set-cookie', 'remote_addr'];

// Or make it configurable through integration options
```

This approach allows users to configure your library in ways that match their framework conventions while maintaining strong typing and validation.