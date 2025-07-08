---
title: Environment variables for configurations
description: Store all configurable values such as URLs, API endpoints, and external
  service locations in environment variables rather than hardcoding them in the codebase.
  This makes the application more maintainable, secure, and environment-adaptable.
repository: prowler-cloud/prowler
label: Configurations
language: TSX
comments_count: 2
repository_stars: 11834
---

Store all configurable values such as URLs, API endpoints, and external service locations in environment variables rather than hardcoding them in the codebase. This makes the application more maintainable, secure, and environment-adaptable.

**Good practice:**
```typescript
// Define the environment variable in your .env file
// NEXT_PUBLIC_RSS_FEED_URL=https://prowler.com/blog/rss

// Then access it directly in your code
const feedUrl = process.env.NEXT_PUBLIC_RSS_FEED_URL;
```

**Avoid:**
```typescript
// Hardcoding configuration values
const RSS_FEED_URL = "https://prowler.com/blog/rss";
```

For values that combine environment variables with runtime data, access the environment variables directly rather than creating unnecessary intermediate variables:

```typescript
// Better approach
const cloudFormationUrl = `${process.env.NEXT_PUBLIC_AWS_CLOUDFORMATION_QUICK_LINK}${session?.tenantId}`;

// Rather than
const CLOUDFORMATION_QUICK_LINK = process.env.NEXT_PUBLIC_AWS_CLOUDFORMATION_QUICK_LINK;
const cloudFormationUrl = `${CLOUDFORMATION_QUICK_LINK}${session?.tenantId}`;
```

This approach improves maintainability, simplifies deployment across different environments, and reduces security risks associated with hardcoded values.