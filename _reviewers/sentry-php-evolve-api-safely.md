---
title: Evolve API safely
description: When modifying existing APIs, implement changes that maintain backward
  compatibility while enabling new functionality. For public-facing APIs, avoid breaking
  changes outside of major version bumps.
repository: getsentry/sentry-php
label: API
language: PHP
comments_count: 7
repository_stars: 1873
---

When modifying existing APIs, implement changes that maintain backward compatibility while enabling new functionality. For public-facing APIs, avoid breaking changes outside of major version bumps.

Key strategies:
1. **Optional parameters**: Add new parameters as optional with sensible defaults
2. **Implementation tricks**: Use `func_get_args()` for parameters that would break signatures
3. **Proper deprecation**: Mark obsolete methods with `@deprecated` and trigger deprecation notices
4. **Clear API boundaries**: Use `@internal` annotations for components not meant for public consumption

```php
// AVOID (breaking change):
public function startTransaction(TransactionContext $context, array $customSamplingContext): Transaction;

// BETTER (backward compatible):
public function startTransaction(TransactionContext $context, ?array $customSamplingContext = null): Transaction;

// OR use implementation tricks:
public function startTransaction(TransactionContext $context): Transaction
{
    // Handle optional parameter without changing signature
    $customSamplingContext = func_num_args() > 1 ? func_get_arg(1) : null;
    
    // Implementation
}

// For deprecating methods:
/**
 * @deprecated since version 2.2, to be removed in 3.0
 */
public function legacyMethod(): void
{
    @trigger_error(sprintf('Method %s() is deprecated since version 2.2 and will be removed in 3.0.', __METHOD__), E_USER_DEPRECATED);
    
    // Call new implementation or keep legacy code
}
```