---
title: Avoid generic suffixes
description: Avoid using generic suffixes like "Response", "Result", or "Request"
  in type names, especially for non-request types. Instead, use semantic names that
  describe the actual data structure and can be reused throughout the codebase.
repository: cline/cline
label: Naming Conventions
language: Other
comments_count: 4
repository_stars: 48299
---

Avoid using generic suffixes like "Response", "Result", or "Request" in type names, especially for non-request types. Instead, use semantic names that describe the actual data structure and can be reused throughout the codebase.

Generic suffixes make types less reusable and create unnecessary coupling to specific API contexts. Semantic names promote code reuse and better express the domain concepts.

Example:
```proto
// Avoid
message AvailableTerminalProfilesResponse {
  repeated string profiles = 1;
}

message StringArrayResponse {
  repeated string values = 1;
}

// Prefer
message TerminalProfiles {
  repeated string profiles = 1;
}

message StringArray {
  repeated string values = 1;
}
```

This approach makes types more generic and reusable across different parts of the codebase, not just in API handlers.