---
title: Document code behavior
description: 'Document the "why" and "how" of your code, not just what it does. Add
  clear comments to explain:


  1. Non-obvious behaviors and edge cases

  2. Special input handling and transformations'
repository: gin-gonic/gin
label: Documentation
language: Go
comments_count: 6
repository_stars: 83022
---

Document the "why" and "how" of your code, not just what it does. Add clear comments to explain:

1. Non-obvious behaviors and edge cases
2. Special input handling and transformations
3. Implementation rationale for tests
4. Usage examples for new APIs

Follow Go documentation conventions: use `//` for comments, don't use dashes after function names, and follow the format: `// FunctionName verb phrase`.

Examples:

```go
// Bad
func TestBindingBSON(t *testing.T) {
    data, _ := bson.Marshal(&obj)
    testBodyBinding(t, BSON, "bson", "/", "/", string(data), string(data[1:]))
}

// Good
func TestBindingBSON(t *testing.T) {
    data, _ := bson.Marshal(&obj)
    // Slicing the first byte simulates invalid BSON input for testing error handling
    testBodyBinding(t, BSON, "bson", "/", "/", string(data), string(data[1:]))
}

// Bad
if val == "" {
    // Code that handles empty values

// Good
if val == "" {
    // Empty string values are intentionally mapped to zero time to avoid parsing errors
    
// Bad
// RunLimited - use netutil.LimitListener to limit inbound accepts

// Good
// RunLimited attaches the router to a http.Server and starts listening and 
// serving HTTP requests using netutil.LimitListener to limit inbound accepts
```

Document behavior of both exported and non-exported elements when they implement important functionality. Include usage examples for new APIs, especially when they introduce patterns like `go:embed`.