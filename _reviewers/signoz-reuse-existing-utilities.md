---
title: reuse existing utilities
description: Before creating new utility functions, check if existing ones can be
  reused or extended. Avoid code duplication by leveraging established utilities and
  creating single sources of truth for repeated patterns.
repository: SigNoz/signoz
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 23369
---

Before creating new utility functions, check if existing ones can be reused or extended. Avoid code duplication by leveraging established utilities and creating single sources of truth for repeated patterns.

When you encounter repeated conditional logic or similar functionality across multiple places, consolidate it into a centralized solution. For example, instead of duplicating conditional assignments based on feature flags throughout the codebase, create a mapping object or utility function that serves as the single source of truth.

Example of what to avoid:
```typescript
// Multiple places with similar conditional logic
aggregateAttribute: dotMetricsEnabled 
  ? 'kafka.consumer.group.lag' 
  : 'kafka_consumer_group_lag'

// In another file
metricName: dotMetricsEnabled 
  ? 'kafka.producer.records' 
  : 'kafka_producer_records'
```

Example of preferred approach:
```typescript
// Create a centralized mapping
const getMetricKey = (baseKey: string, dotMetricsEnabled: boolean) => {
  const metricKeyMap = {
    'kafka_consumer_group_lag': 'kafka.consumer.group.lag',
    'kafka_producer_records': 'kafka.producer.records'
  };
  return dotMetricsEnabled ? metricKeyMap[baseKey] : baseKey;
};

// Use existing formatting utilities instead of creating new ones
const formattedValue = getYAxisFormattedValue(value, format);
```

This approach improves maintainability, reduces the risk of inconsistencies, and makes the codebase easier to understand and modify.