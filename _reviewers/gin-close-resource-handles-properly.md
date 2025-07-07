---
title: Close resource handles properly
description: Always close file resources and other system handles after use to prevent
  resource leaks. Resource leaks can cause system instability, memory issues, and
  limit scalability, especially in long-running services handling many requests.
repository: gin-gonic/gin
label: Error Handling
language: Markdown
comments_count: 2
repository_stars: 83022
---

Always close file resources and other system handles after use to prevent resource leaks. Resource leaks can cause system instability, memory issues, and limit scalability, especially in long-running services handling many requests.

For example, when working with files or similar resources:

```go
// BAD: Resource leak
func handleUpload(c *gin.Context) {
    file, _ := c.Request.FormFile("upload")
    // file is never closed
    // process file...
}

// GOOD: Properly closed resource
func handleUpload(c *gin.Context) {
    file, err := c.Request.FormFile("upload")
    if err != nil {
        // Handle error
        return
    }
    defer file.Close() // Always close the file
    
    // process file...
}
```

For more complex scenarios, ensure resources are closed even when errors occur. The `defer` statement in Go is particularly useful for this purpose as it guarantees execution even if the function returns early due to an error. When managing multiple resources, close them in the reverse order of acquisition to avoid dependency issues.