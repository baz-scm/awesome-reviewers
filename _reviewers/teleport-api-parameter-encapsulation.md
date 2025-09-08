---
title: API parameter encapsulation
description: When designing API methods that accept multiple related parameters (especially
  filters, search criteria, or configuration options), encapsulate them in dedicated
  message types rather than adding individual fields directly to the request message.
  This pattern improves future extensibility by allowing new parameters to be added
  without breaking existing...
repository: gravitational/teleport
label: API
language: Other
comments_count: 3
repository_stars: 19109
---

When designing API methods that accept multiple related parameters (especially filters, search criteria, or configuration options), encapsulate them in dedicated message types rather than adding individual fields directly to the request message. This pattern improves future extensibility by allowing new parameters to be added without breaking existing method signatures.

For example, instead of adding individual filter fields:
```proto
message ListAccessListsRequest {
  int32 page_size = 1;
  string next_token = 2;
  string search = 3;           // Avoid this
  types.SortBy sort_by = 4;    // Avoid this
}
```

Encapsulate related parameters in a dedicated message:
```proto
message ListAccessListsRequest {
  int32 page_size = 1;
  string next_token = 2;
  ListAccessListsFilter filter = 3;  // Preferred approach
}

message ListAccessListsFilter {
  string search = 1;
  repeated string owners = 2;
  repeated string roles = 3;
}
```

This approach has several benefits: it makes the API more organized and self-documenting, enables adding new filter options without changing method signatures, allows for generic helper functions that can work with filter types, and provides a clear upgrade path when backward compatibility concerns require creating new API versions (e.g., ListAccessListsV2). When extending existing APIs would break backward compatibility, consider creating versioned methods rather than modifying existing ones.