---
title: AI provider naming clarity
description: Use specific, unambiguous names for AI providers and models to prevent
  confusion when working with multiple AI services. Avoid generic names that could
  be mistaken for other providers or create ambiguity about the underlying service.
repository: cline/cline
label: AI
language: TypeScript
comments_count: 3
repository_stars: 48299
---

Use specific, unambiguous names for AI providers and models to prevent confusion when working with multiple AI services. Avoid generic names that could be mistaken for other providers or create ambiguity about the underlying service.

When naming AI providers:
- Use provider-specific prefixes (e.g., "huawei-cloud-maas" instead of generic "maas")
- Include explicit provider suffixes when beneficial for discoverability (e.g., "moonshotai/Kimi-K2-Instruct:groq")
- Rename providers when the connection between name and service is unclear

Example from discussions:
```typescript
// Before: Confusing connection between Oracle and LiteLLM
// After: Rename to "oca_" for clarity

// Before: Generic interface name
interface HuaweiCloudMaaSHandlerOptions {
    huaweiCloudMaasApiKey?: string
}

// After: Huawei-specific naming
interface HuaweiCloudMaaSHandlerOptions {
    huaweiCloudMaasApiKey?: string  // Clear this is Huawei-specific
}

// Include explicit provider suffixes for discoverability
"moonshotai/Kimi-K2-Instruct:groq": {
    // model configuration
}
```

This prevents developer confusion, improves code maintainability, and makes the relationship between code and AI services immediately clear.