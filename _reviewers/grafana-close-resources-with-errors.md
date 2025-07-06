---
title: Close resources with errors
description: Always close resources (files, streams, connections) and properly handle
  their Close() errors. For read operations, Close() errors can be ignored if the
  primary operation (like JSON parsing) succeeded. For write operations, always check
  and propagate Close() errors.
repository: grafana/grafana
label: Error Handling
language: Go
comments_count: 5
repository_stars: 68825
---

Always close resources (files, streams, connections) and properly handle their Close() errors. For read operations, Close() errors can be ignored if the primary operation (like JSON parsing) succeeded. For write operations, always check and propagate Close() errors.

Example:
```go
// Bad:
data, err := io.ReadAll(reader)
reader.Close() // Error ignored!

// Good for reads:
defer reader.Close()
var result MyStruct
err := json.NewDecoder(reader).Decode(&result)
return result, err

// Good for writes:
writer := getWriter()
defer func() {
    if closeErr := writer.Close(); err == nil {
        err = closeErr // Only propagate Close error if no other error occurred
    }
}()
return writer.Write(data)
```

This practice prevents resource leaks and ensures data integrity, especially for write operations where Close() errors could indicate incomplete writes or corruption.