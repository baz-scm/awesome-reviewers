---
title: Review configuration currency
description: Regularly audit and update configuration to align with current tool capabilities
  and best practices. Remove obsolete settings that are no longer needed due to tool
  evolution, and consolidate fragmented configuration approaches into more unified
  solutions.
repository: mastodon/mastodon
label: Configurations
language: JavaScript
comments_count: 2
repository_stars: 48691
---

Regularly audit and update configuration to align with current tool capabilities and best practices. Remove obsolete settings that are no longer needed due to tool evolution, and consolidate fragmented configuration approaches into more unified solutions.

When underlying tools gain new capabilities, review existing configuration to identify opportunities for simplification. For example, when build tools natively support language features, remove explicit transformation rules. When libraries provide consolidated configuration options, prefer them over fragmented environment variables.

Example from database configuration:
```javascript
// Avoid fragmented approach with multiple environment variables
if (env.DB_SSLMODE) {
  logger.warn(
    'Using DB_SSLMODE is not recommended, instead use DATABASE_URL with SSL options',
  );
}

// Prefer consolidated configuration
config = toClientConfig(parse(env.DATABASE_URL, { useLibpqCompat: true }));
```

Establish a regular review cycle to assess whether configuration reflects current standards and tool capabilities. Document the reasoning behind configuration choices to help future maintainers understand when updates may be appropriate.