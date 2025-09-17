---
title: Optimize database queries
description: When writing database queries, prioritize both performance and correctness.
  Avoid unnecessary joins that can significantly impact query performance - fetch
  only essential data and use separate services or caches for additional lookups.
  Also ensure your filtering logic doesn't inadvertently exclude valid records, particularly
  with boundary conditions.
repository: unionlabs/union
label: Database
language: TypeScript
comments_count: 2
repository_stars: 74800
---

When writing database queries, prioritize both performance and correctness. Avoid unnecessary joins that can significantly impact query performance - fetch only essential data and use separate services or caches for additional lookups. Also ensure your filtering logic doesn't inadvertently exclude valid records, particularly with boundary conditions.

For performance optimization, prefer fetching minimal data:
```typescript
// Instead of expensive joins for display names
newer: v0_transfers(
  where: { source_timestamp: { _gt: $timestamp } }
) {
  source_chain { chain_id display_name }  // Adds expensive joins
}

// Fetch IDs only and use separate service
newer: v0_transfers(
  where: { source_timestamp: { _gt: $timestamp } }
) {
  source_chain { chain_id }  // Minimal data
}
// Then use chainsgate service for display names
```

For correctness, ensure filters cover boundary cases:
```typescript
// Problematic - misses exact timestamp matches
where: { source_timestamp: { _gt: $timestamp } }
where: { source_timestamp: { _lt: $timestamp } }

// Better - includes boundary values
where: { source_timestamp: { _gte: $timestamp } }
where: { source_timestamp: { _lte: $timestamp } }
```