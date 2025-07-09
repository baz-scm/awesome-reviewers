---
title: Hierarchical semantic naming
description: Use hierarchical prefixes and clear descriptive names to indicate the
  domain, source, and purpose of code elements. This improves code organization, searchability,
  and helps maintain consistency across the codebase.
repository: neondatabase/neon
label: Naming Conventions
language: Other
comments_count: 5
repository_stars: 19015
---

Use hierarchical prefixes and clear descriptive names to indicate the domain, source, and purpose of code elements. This improves code organization, searchability, and helps maintain consistency across the codebase.

For metrics:
- Start with the component name (e.g., `compute_`)
- Add the data source if applicable (e.g., `pg_` for PostgreSQL data)
- Finish with a semantically accurate description (e.g., `oldest_frozen_xid_age`)

For API methods:
- Follow established style guides (e.g., Google's recommendation to use verbs in method names)
- Use specific, descriptive names rather than generic ones (e.g., `GetDbSize` instead of `DbSize`)
- Group related fields and use consistent prefixing (e.g., `request_id`, `request_class`)

Example:
```
// Metrics:
compute_pg_oldest_frozen_xid_age  // Not: frozen_xid_age or compute_min_mxid_age

// API Methods:
rpc GetDbSize (DbSizeRequest) returns (DbSizeResponse);  // Not: DbSize

// Message fields:
message GetPageRequest {
  uint64 request_id = 1;    // Consistent prefixing for request metadata
  RequestLsn read_lsn = 2;  // Specific, descriptive name vs. "common"
}
```

This avoids ambiguity, improves code readability, and makes the codebase more maintainable.