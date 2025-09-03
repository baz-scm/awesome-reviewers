---
title: exported functions documentation
description: All exported functions, types, and methods must include Go-style documentation
  comments that clearly explain their purpose, parameters, return values, and usage.
  This is a fundamental requirement for code quality and maintainability.
repository: avelino/awesome-go
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 151435
---

All exported functions, types, and methods must include Go-style documentation comments that clearly explain their purpose, parameters, return values, and usage. This is a fundamental requirement for code quality and maintainability.

The documentation comments should:
- Start with the function/type name
- Provide a clear, concise explanation of what it does
- Document all parameters and return values
- Include usage examples when helpful
- Be written in English for broad accessibility

Example of proper Go-style documentation:

```go
// Get makes an HTTP GET request through the proxy pool with automatic
// retries and load balancing. It returns the response body and any error
// encountered during the request.
func Get(url string) (*http.Response, error) {
    // implementation
}

// Client represents an HTTP client with proxy pool capabilities
// for fault tolerance and load balancing.
type Client struct {
    // fields
}
```

This requirement ensures that all public APIs are self-documenting and accessible to other developers. Projects lacking proper documentation comments for exported elements should not be accepted until this standard is met, as it directly impacts the usability and professional quality of the codebase.