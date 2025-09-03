---
title: Observability correctness and maintainability
description: Ensure observability implementations prioritize both mathematical correctness
  and code maintainability. Observability systems must produce accurate metrics and
  telemetry data while remaining easy to understand and modify.
repository: SigNoz/signoz
label: Observability
language: Go
comments_count: 2
repository_stars: 23369
---

Ensure observability implementations prioritize both mathematical correctness and code maintainability. Observability systems must produce accurate metrics and telemetry data while remaining easy to understand and modify.

For metric calculations, verify that aggregation operations are mathematically sound. Changing aggregation types (like countDistinct to count) requires careful consideration of their semantic differences and impact on data accuracy.

For telemetry tracking code, refactor complex logic into simpler, more maintainable structures. Consolidate duplicate tracking logic and use consistent patterns for event properties.

Example of maintaining correctness:
```go
// Before: Incorrect aggregation change
AggregateOperator: v3.AggregateOperatorCount, // Wrong for distinct URLs

// After: Correct aggregation or proper alternative
AggregateOperator: v3.AggregateOperatorCountDistinct, // Correct for unique URLs
// OR use count with span_id if semantically equivalent
```

Example of improving maintainability:
```go
// Before: Complex, duplicated telemetry logic with nested conditions
if alertMatched || dashboardMatched {
    // 50+ lines of duplicated tracking logic
}

// After: Simplified, consolidated approach
queryInfoResult := NewQueryInfoResult(queryRangeParams, version)
aH.Signoz.Analytics.TrackUser(ctx, orgID, userID, "Telemetry Queried", queryInfoResult.ToMap())
```

Remember that correctness is non-negotiable in observability systems - users depend on accurate metrics for critical decisions about system health and performance.