---
title: Avoid hardcoded configurations
description: Always parameterize values that might vary across different environments
  or users instead of hardcoding them in your code. This applies to API endpoints,
  regions, dimensions, credentials, and other configuration values.
repository: langchain-ai/langchainjs
label: Configurations
language: TypeScript
comments_count: 4
repository_stars: 15004
---

Always parameterize values that might vary across different environments or users instead of hardcoding them in your code. This applies to API endpoints, regions, dimensions, credentials, and other configuration values.

When providing fallbacks to environment variables, use nullish coalescing (`??`) to only override missing values rather than replacing all values if any are missing:

```typescript
// ❌ Don't do this
if (!id || !secret || !uri) {
  id = getEnvironmentVariable("OUTLOOK_CLIENT_ID");
  secret = getEnvironmentVariable("OUTLOOK_CLIENT_SECRET");
  uri = getEnvironmentVariable("OUTLOOK_REDIRECT_URI");
}

// ✅ Do this instead
id = id ?? getEnvironmentVariable("OUTLOOK_CLIENT_ID");
secret = secret ?? getEnvironmentVariable("OUTLOOK_CLIENT_SECRET");
uri = uri ?? getEnvironmentVariable("OUTLOOK_REDIRECT_URI");
```

For service defaults, prefer leaving values unset when possible and let the backend/service set the defaults. This prevents issues when service providers change their best practices:

```typescript
// ❌ Don't hardcode dimensions, regions, endpoints, etc.
vectorSearchDimensions: 1536, // Hardcoded to ada-002's size

// ✅ Make these configurable via parameters
vectorSearchDimensions: config.dimensions || embeddings.dimensions,
```

When integrating with SDKs, only pass overridden values and avoid setting unnecessary defaults:

```typescript
// ❌ Don't do this
const app = new FirecrawlApp({ apiKey: this.apiKey, apiUrl: "https://api.firecrawl.dev" });

// ✅ Do this instead
const params = { apiKey: this.apiKey };
if (this.apiUrl !== undefined) {
  params.apiUrl = this.apiUrl;
}
const app = new FirecrawlApp(params);
```
