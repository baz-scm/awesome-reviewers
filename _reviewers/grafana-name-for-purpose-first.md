---
title: Name for purpose first
description: Choose names that lead with their primary purpose or category, followed
  by specific details. This makes code more discoverable and self-documenting by grouping
  related items and clearly conveying intent.
repository: grafana/grafana
label: Naming Conventions
language: Go
comments_count: 4
repository_stars: 68825
---

Choose names that lead with their primary purpose or category, followed by specific details. This makes code more discoverable and self-documenting by grouping related items and clearly conveying intent.

Key guidelines:
- Start with the general category/area (e.g., 'sharing', 'render', 'sanitize')
- Follow with specific details or actions
- Avoid legacy/implementation prefixes unless specifically needed
- Use directional words when transforming between formats

Example:
```go
// Less clear:
func sanitizeGrpcHeaderValue(value string) string {}
func dashboardImageSharing() {}

// More clear:
func sanitizeHTTPHeaderValueForGRPC(value string) string {}
func sharingDashboardImage() {}
```

This pattern helps when:
- Searching for related functionality
- Understanding transformation direction
- Grouping related features
- Maintaining consistent terminology