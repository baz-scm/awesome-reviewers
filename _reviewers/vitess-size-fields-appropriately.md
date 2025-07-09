---
title: Size fields appropriately
description: When designing database schemas, choose field types and sizes that accommodate
  both current and anticipated future data volumes. Undersized fields can cause production
  issues and limit functionality when data grows beyond initial expectations. Additionally,
  ensure consistency between related fields that store similar data or participate
  in the same...
repository: vitessio/vitess
label: Database
language: Sql
comments_count: 2
repository_stars: 19815
---

When designing database schemas, choose field types and sizes that accommodate both current and anticipated future data volumes. Undersized fields can cause production issues and limit functionality when data grows beyond initial expectations. Additionally, ensure consistency between related fields that store similar data or participate in the same operations.

Example:
```sql
-- Avoid restrictive size limits for fields that may grow
-- Bad:
`pos`       varbinary(10000) NOT NULL,
`stop_pos`  varbinary(10000) DEFAULT NULL,

-- Better:
`pos`       mediumblob NOT NULL,        -- Up to 16MB
`stop_pos`  mediumblob DEFAULT NULL,    -- Matching type and capacity
```

For fields containing potentially large data (like position coordinates, serialized objects, or binary data), prefer types with sufficient headroom rather than arbitrary size limitations. This prevents operational issues when edge cases are encountered in production.