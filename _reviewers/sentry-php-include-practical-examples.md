---
title: Include practical examples
description: 'Enhance technical documentation with clear, practical code examples
  that demonstrate usage. This applies to:


  1. Changelog entries for new features

  2. API documentation'
repository: getsentry/sentry-php
label: Documentation
language: Markdown
comments_count: 4
repository_stars: 1873
---

Enhance technical documentation with clear, practical code examples that demonstrate usage. This applies to:

1. Changelog entries for new features
2. API documentation
3. Contributing guidelines
4. Migration/upgrade guides

Good documentation with examples reduces confusion, speeds up implementation, and prevents common mistakes. When documenting changes or new functionality, clearly explain what it does and provide sample code showing proper usage.

Example of an improved changelog entry:

```
### Features

- Add timing span when emiting a timing metric [(#1717)](https://github.com/getsentry/sentry-php/pull/1717)

  ```php
  // Example usage
  $metric = new Timing('database.query', 42.0);
  $metric->setSpanStatus(SpanStatus::OK);
  $metric->setUnit(DurationUnit::MILLISECOND);
  ```
```

For migration guides, show both old and new approaches side by side to help users understand the transition. Clear examples are especially important when explaining complex changes or features that might be unintuitive.