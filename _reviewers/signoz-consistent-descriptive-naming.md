---
title: consistent descriptive naming
description: Use meaningful, descriptive names that clearly convey purpose and maintain
  consistency across similar concepts throughout the codebase. Avoid magic strings,
  cryptic abbreviations, and inconsistent naming patterns.
repository: SigNoz/signoz
label: Naming Conventions
language: Go
comments_count: 12
repository_stars: 23369
---

Use meaningful, descriptive names that clearly convey purpose and maintain consistency across similar concepts throughout the codebase. Avoid magic strings, cryptic abbreviations, and inconsistent naming patterns.

Key principles:
1. **Replace magic strings with constants**: Instead of `"clickhouse_max_threads"`, create `const ClickhouseMaxThreadsKey = "clickhouse_max_threads"`
2. **Use consistent naming patterns**: If using "legacy/current" convention in one place, apply it consistently elsewhere (e.g., `serverAddrLegacyIdx` and `serverAddrCurrentIdx` instead of mixing `serverAddrIdx` and `netPeerIdx`)
3. **Choose descriptive variable names**: Replace cryptic names like `k, m` with meaningful ones like `metricName, isNormalized`
4. **Use semantic function names**: `GetTransitionedMetric` (singular) instead of `GetTransitionedMetrics` when operating on single items
5. **Follow established conventions**: Use `NewNotFoundf` instead of `NotFoundNew` for natural readability, and `Start/End` instead of `StartDate/EndDate` for timestamp fields
6. **Maintain naming consistency across similar concepts**: Use `alert_id` consistently if other IDs follow underscore convention

Example of good naming consistency:
```go
const (
    ServerNameLegacyKey  = "net.peer.name"
    ServerNameCurrentKey = "server.address"
    URLPathLegacyKey     = "http.url" 
    URLPathCurrentKey    = "url.full"
)

// Consistent variable naming
serverAddrLegacyIdx := -1
serverAddrCurrentIdx := -1
```

This approach improves code readability, reduces confusion during reviews, and makes the codebase more maintainable by establishing clear naming patterns that developers can follow consistently.