---
title: API response standardization
description: Ensure API responses follow established patterns and use proper typing.
  Always use standardized response types like `PaginatedResponse` for paginated endpoints,
  avoid hardcoded union types for dynamic values that should be strings, and return
  fresh data from API responses rather than stale local data.
repository: PostHog/posthog
label: API
language: TypeScript
comments_count: 4
repository_stars: 28460
---

Ensure API responses follow established patterns and use proper typing. Always use standardized response types like `PaginatedResponse` for paginated endpoints, avoid hardcoded union types for dynamic values that should be strings, and return fresh data from API responses rather than stale local data.

Key practices:
- Use established response patterns: `PaginatedResponse<T>` for paginated APIs
- Prefer flexible string types over hardcoded unions for dynamic values (e.g., sync names like "Stripe")
- Return updated data from API responses, not the original request data
- Create reusable type definitions instead of complex inline types

Example:
```typescript
// Bad: Hardcoded union types and inline complex types
async recentActivity(): Promise<{
    activities: Array<{
        type: 'external_data_sync' | 'materialized_view'  // Too rigid
    }>
}> 

// Good: Standardized response with flexible types
type FunctionActionType = 'function' | 'function_email' | 'function_sms' | 'function_slack' | 'function_webhook';

async recentActivity(): Promise<PaginatedResponse<ActivityItem>> {
    // Use string for dynamic sync names like "Stripe", "Salesforce"
    type: string  // More flexible for dynamic values
}

// Always return fresh API data
const updatedSource = await api.externalDataSources.update(source.id, source)
return {
    ...values.dataWarehouseSources,
    results: values.dataWarehouseSources?.results.map((s) => 
        s.id === updatedSource.id ? updatedSource : s  // Use fresh data
    ) || []
}
```