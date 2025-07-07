---
title: Write resilient tests
description: Tests should be designed to validate behavior without being brittle or
  sensitive to implementation details. Avoid direct string comparisons for complex
  data structures or binary data, as these tests can break due to formatting changes
  or encoding issues that don't reflect actual functional problems.
repository: gin-gonic/gin
label: Testing
language: Go
comments_count: 3
repository_stars: 83022
---

Tests should be designed to validate behavior without being brittle or sensitive to implementation details. Avoid direct string comparisons for complex data structures or binary data, as these tests can break due to formatting changes or encoding issues that don't reflect actual functional problems.

Instead:
1. For binary data, compare raw byte slices:
```go
// Instead of this (brittle):
assert.Equal(t, string(bsonData), w.Body.String())

// Do this (more robust):
assert.Equal(t, bsonData, w.Body.Bytes())
```

2. For structured data like JSON/YAML/XML, unmarshal back to a comparable structure:
```go
// Instead of string comparisons:
assert.Equal(t, "{\"foo\":\"bar\"}", w.Body.String())

// Parse and compare structurally:
var result map[string]interface{}
err := json.Unmarshal(w.Body.Bytes(), &result)
require.NoError(t, err)
assert.Equal(t, expectedData, result)
```

3. For complex strings with variable ordering (like HTTP headers):
```go
// Instead of exact string matching:
assert.Equal(t, "user=gin; Path=/; Domain=localhost; Max-Age=1; HttpOnly; Secure", cookie)

// Check each component individually:
setCookie := w.Header().Get("Set-Cookie")
assert.Contains(t, setCookie, "user=gin")
assert.Contains(t, setCookie, "Path=/")
assert.Contains(t, setCookie, "Domain=localhost")
```

These approaches ensure tests remain valid even when non-functional aspects of the implementation change, reducing maintenance burden and avoiding false test failures.