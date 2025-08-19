---
title: Optimize database query patterns
description: Avoid N+1 query problems and overly complex conditional SQL construction.
  When loading related data, prefer batch operations or dedicated endpoints that can
  fetch all required data in fewer queries. For conditional SQL parameters, consider
  using null values with database defaults instead of constructing different query
  strings.
repository: PostHog/posthog
label: Database
language: TypeScript
comments_count: 2
repository_stars: 28460
---

Avoid N+1 query problems and overly complex conditional SQL construction. When loading related data, prefer batch operations or dedicated endpoints that can fetch all required data in fewer queries. For conditional SQL parameters, consider using null values with database defaults instead of constructing different query strings.

Example of the problem:
```typescript
// Avoid: Multiple individual requests (N+1 pattern)
const results = await Promise.all(
    dataSources.map(async (source) => {
        const jobs = await api.externalDataSources.jobs(source.id, monthStartISO, null)
        return sumMTDRows(jobs, monthStartISO)
    })
)

// Avoid: Complex conditional SQL construction
const query = forcedId 
    ? `INSERT INTO posthog_person (id, created_at, ...) VALUES ($1, $2, ...)`
    : `INSERT INTO posthog_person (created_at, ...) VALUES ($1, $2, ...)`
```

Better approaches:
```typescript
// Prefer: Single batch request
const allJobsData = await api.externalDataSources.batchJobs(dataSourceIds, monthStartISO)

// Prefer: Always include parameter, use null for auto-increment
const query = `INSERT INTO posthog_person (id, created_at, ...) VALUES ($1, $2, ...)`
// Pass null for id when auto-increment is desired
```

This reduces database load, improves performance, and simplifies code maintenance by eliminating conditional query construction.