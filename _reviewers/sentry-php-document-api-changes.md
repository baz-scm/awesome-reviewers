---
title: Document API changes
description: 'When documenting API changes, particularly breaking changes, follow
  these practices to ensure clarity and ease of migration:


  1. **Group related changes** for better scannability. When multiple methods or functions
  change in a similar way, format them as a structured list:'
repository: getsentry/sentry-php
label: API
language: Markdown
comments_count: 5
repository_stars: 1873
---

When documenting API changes, particularly breaking changes, follow these practices to ensure clarity and ease of migration:

1. **Group related changes** for better scannability. When multiple methods or functions change in a similar way, format them as a structured list:
```
- The following methods now return `EventId` instead of `string`:
  - `ClientInterface::captureMessage()`
  - `ClientInterface::captureException()`
  - `HubInterface::captureEvent()`
```

2. **Provide explicit migration paths** whenever removing or changing API functionality. Always include the recommended alternative:
```
- Removed the following methods from `ClientBuilderInterface`, use `ClientBuilderInterface::setTransportFactory()` instead:
  - `setUriFactory()`
  - `setHttpClient()`
```

3. **Link to relevant specifications or standards** when referencing them in API changes to provide context:
```
- Refactor to support the [Unified API SDK specs](https://docs.sentry.io/development/sdk-dev/unified-api/)
```

4. **Clearly indicate public API changes** by explicitly documenting when internal components become part of the public API:
```
- Make the `StacktraceBuilder` class part of the public API and add the `Client::getStacktraceBuilder()` method
```

These practices ensure that developers can easily understand changes, assess impact, and migrate their code efficiently.