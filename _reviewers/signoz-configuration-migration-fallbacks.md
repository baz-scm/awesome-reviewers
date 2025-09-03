---
title: Configuration migration fallbacks
description: When configuration structures evolve, implement fallback mechanisms to
  handle both old and new formats gracefully. This ensures backward compatibility
  during transitions and prevents breaking changes.
repository: SigNoz/signoz
label: Configurations
language: TSX
comments_count: 2
repository_stars: 23369
---

When configuration structures evolve, implement fallback mechanisms to handle both old and new formats gracefully. This ensures backward compatibility during transitions and prevents breaking changes.

Key practices:
- Check for new configuration format first, then fall back to legacy format
- Update conversion logic when units or data types change
- Provide clear migration paths for deprecated configuration options

Example from query configuration migration:
```typescript
// Check new format first, then fallback to legacy
metricName: queryData.aggregation?.[0].metricName || queryData.aggregateAttribute?.key
```

Example from TTL configuration update:
```typescript
// Handle unit conversion during configuration migration
setLogsCurrentTTLValues((prev) => ({
  ...prev,
  logs_ttl_duration_hrs: logsTotalRetentionPeriod || -1,
  default_ttl_days: logsTotalRetentionPeriod 
    ? logsTotalRetentionPeriod / 24 // convert Hours to days
    : prev.default_ttl_days
}));
```

This approach maintains system stability while allowing configuration schemas to evolve over time.