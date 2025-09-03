---
title: API payload completeness
description: 'Ensure all required fields are included in API payloads and handle special
  field cases properly to prevent runtime errors and data inconsistencies.


  Missing fields in API transformations can cause bugs and unexpected behavior. Always
  validate that essential fields like `aggregations`, `filter`, and `having` are properly
  passed through data transformations....'
repository: SigNoz/signoz
label: API
language: TypeScript
comments_count: 3
repository_stars: 23369
---

Ensure all required fields are included in API payloads and handle special field cases properly to prevent runtime errors and data inconsistencies.

Missing fields in API transformations can cause bugs and unexpected behavior. Always validate that essential fields like `aggregations`, `filter`, and `having` are properly passed through data transformations. Additionally, handle special cases where certain fields require different treatment based on context.

For example, when transforming query data, ensure all necessary fields are preserved:

```typescript
queryData.push({
    ...baseQuery,
    filters: queryFromData.filters,
    filter: queryFromData.filter,        // Don't forget these
    aggregations: queryFromData.aggregations,  // Missing causes bugs
    having: queryFromData.having,
});
```

When dealing with special fields, implement proper conditional logic:

```typescript
const fieldObj: TelemetryFieldKey = {
    name: fieldName,
    fieldDataType: column?.fieldDataType ?? (column?.dataType as FieldDataType),
    signal: column?.signal ?? undefined,
};

// Only add fieldContext if the field is NOT deprecated
if (!isDeprecated && fieldName !== 'name') {
    fieldObj.fieldContext = column?.fieldContext ?? (column?.type as FieldContext);
}
```

Always consider how missing or incorrectly structured fields will affect downstream API consumers and implement comprehensive field validation before sending payloads.