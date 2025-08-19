---
title: optimize data loading
description: Review data loading operations to ensure they are properly scoped, filtered,
  and batched to prevent performance issues. Large datasets should be handled with
  appropriate pagination, filtering by relevant criteria (like date ranges), and avoiding
  operations that could load excessive amounts of data into memory.
repository: PostHog/posthog
label: Performance Optimization
language: TypeScript
comments_count: 3
repository_stars: 28460
---

Review data loading operations to ensure they are properly scoped, filtered, and batched to prevent performance issues. Large datasets should be handled with appropriate pagination, filtering by relevant criteria (like date ranges), and avoiding operations that could load excessive amounts of data into memory.

Key areas to check:
- Avoid spread operators with large arrays that could cause memory issues
- Ensure pagination limits don't truncate important data - consider if limits like "last 200 jobs" could miss records in high-volume scenarios
- Apply proper filtering before loading data rather than loading everything and filtering later
- Question whether all requested data is actually needed for the use case

Example of problematic pattern:
```typescript
// Loads ALL jobs for ALL sources without filtering
const allJobs = await Promise.all(
    dataSources.map(async (source) => {
        // This could return 283,914 items for large teams
        return await api.externalDataSources.jobs(source.id, null, null)
    })
)
```

Better approach:
```typescript
// Apply filtering and reasonable limits upfront
const recentJobs = await Promise.all(
    dataSources.map(async (source) => {
        return await api.externalDataSources.jobs(
            source.id, 
            cutoffDate, // Filter by date
            REASONABLE_LIMIT // Appropriate batch size
        )
    })
)
```