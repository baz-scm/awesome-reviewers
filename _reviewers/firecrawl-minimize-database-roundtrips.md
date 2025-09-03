---
title: Minimize database roundtrips
description: Avoid making multiple database queries when a single query can retrieve
  the required data. Each database roundtrip adds latency and increases system load.
  Before making a database call, check if the data is already available or if multiple
  queries can be combined into one.
repository: firecrawl/firecrawl
label: Database
language: TypeScript
comments_count: 2
repository_stars: 54535
---

Avoid making multiple database queries when a single query can retrieve the required data. Each database roundtrip adds latency and increases system load. Before making a database call, check if the data is already available or if multiple queries can be combined into one.

Common patterns to avoid:
- Making separate queries for the same entity (e.g., checking permissions then fetching full data)
- Sequential queries that could be batched
- Redundant validation queries when data can be validated in the main query

Example of inefficient pattern:
```typescript
// Inefficient: Two separate queries for the same job
const job = await supabaseGetJobByIdOnlyData(req.params.jobId);
if (!job || job.team_id !== req.auth.team_id) {
  return res.status(403).json({ success: false, error: "Access denied" });
}

const jobData = await supabaseGetJobsById([req.params.jobId]);
```

Better approach:
```typescript
// Efficient: Single query with proper error handling
const jobData = await supabaseGetJobsById([req.params.jobId]);
if (!jobData || jobData.length === 0 || jobData[0].team_id !== req.auth.team_id) {
  return res.status(403).json({ success: false, error: "Access denied or not found" });
}
```

When pagination is necessary due to database limits, ensure it's truly required and document the reasoning clearly.