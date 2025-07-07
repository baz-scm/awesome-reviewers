---
title: Document API behavior
description: 'Thoroughly document how your API endpoints handle data binding and processing,
  especially non-obvious behaviors that affect how client data is mapped to server-side
  structures. This includes:'
repository: gin-gonic/gin
label: API
language: Markdown
comments_count: 2
repository_stars: 83022
---

Thoroughly document how your API endpoints handle data binding and processing, especially non-obvious behaviors that affect how client data is mapped to server-side structures. This includes:

1. Clearly document form tag behaviors and special syntax (like `form:"-"`)
2. Explain how different HTTP methods affect binding logic
3. Document content-type specific behaviors 

For example, when implementing binding in a web framework like Gin, include explanatory comments:

```go
// Person represents data received from API clients
type Person struct {
  Name    string `form:"name"`
  Address string `form:"address"`
  InternalID string `form:"-"` // This field won't be populated from form data
}

func handleRequest(c *gin.Context) {
  var person Person
  
  // Document binding behavior:
  // If `GET`, only `Form` binding engine (`query`) used.
  // If `POST`, first checks the `content-type` for `JSON` or `XML`, then uses `Form` (`form-data`).
  if c.Bind(&person) == nil {
    // Process the data
  }
}
```

Clear API behavior documentation reduces friction for API consumers, minimizes unexpected behaviors, and reduces support burden for your team.