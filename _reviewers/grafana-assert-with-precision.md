---
title: Assert with precision
description: Tests should verify actual behavior rather than just successful execution.
  When writing assertions, favor precise equality checks that verify the exact content
  and ordering rather than loose containment checks.
repository: grafana/grafana
label: Testing
language: Go
comments_count: 2
repository_stars: 68825
---

Tests should verify actual behavior rather than just successful execution. When writing assertions, favor precise equality checks that verify the exact content and ordering rather than loose containment checks.

For tests involving external systems or complex interactions, verify what was actually sent or received rather than just that an operation completed successfully. This ensures the test catches subtle bugs in the data being transmitted.

Example:

```go
// Weak assertion - only checks that elements exist but not complete set or order
require.Contains(t, names, "resource-1")
require.Contains(t, names, "resource-2")

// Strong assertion - verifies exact content and ordering
require.Equal(t, []string{"resource-1", "resource-2"}, names)
```

Similarly, when testing server interactions, verify the exact payload sent to the server:

```go
// Add verification of what the server received
server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
    // Capture and verify what was sent to the server
    require.NoError(t, json.NewDecoder(r.Body).Decode(&configSent))
    require.Equal(t, expectedConfig, configSent)
    
    // Rest of the handler
}))
```

Precise assertions make tests more reliable at catching regressions and unintended changes in behavior.