---
title: Handle errors completely
description: Always handle errors comprehensively by checking return values, implementing
  proper error propagation, and ensuring resources are cleaned up. Errors that are
  ignored or improperly handled can lead to resource leaks, unexpected behavior, or
  application crashes.
repository: fatedier/frp
label: Error Handling
language: Go
comments_count: 5
repository_stars: 95938
---

Always handle errors comprehensively by checking return values, implementing proper error propagation, and ensuring resources are cleaned up. Errors that are ignored or improperly handled can lead to resource leaks, unexpected behavior, or application crashes.

Follow these principles:

1. **Check all error returns**: Never discard errors with blank identifiers (`_`) unless you have explicitly determined the error can be safely ignored.

```go
// Bad
cfg.BandwidthLimit, _ = NewBandwidthQuantity(pMsg.BandwidthLimit) // Ignores error, creating empty bandwidth limit

// Good
cfg.BandwidthLimit, err = NewBandwidthQuantity(pMsg.BandwidthLimit)
if err != nil {
    // Handle appropriately: set default, log warning, or return error
    xl.Warnf("Invalid bandwidth limit %q: %v", pMsg.BandwidthLimit, err)
}
```

2. **Add error returns to functions that can fail**: Ensure callers can detect and handle failures.

```go
// Bad
func (c *Controller) RegisterClientRoute(ctx context.Context, name string, routes []net.IPNet, conn io.ReadWriteCloser) {
    // No way to signal failure to caller
}

// Good
func (c *Controller) RegisterClientRoute(ctx context.Context, name string, routes []net.IPNet, conn io.ReadWriteCloser) error {
    // Implementation
    return err // Return any failure
}
```

3. **Close resources after errors**: Always clean up resources when errors occur.

```go
// Bad
if err := svr.RegisterWorkConn(conn, m); err != nil {
    // Error logged but connection left open
}

// Good
if err := svr.RegisterWorkConn(conn, m); err != nil {
    conn.Close() // Clean up resources
}
```

4. **Protect against panic conditions**: Especially in callbacks or user-provided code.

```go
// Good
if onClose != nil {
    func() {
        defer func() {
            if r := recover(); r != nil {
                xl.Warnf("onClose callback panicked: %v", r)
            }
        }()
        onClose()
    }()
}
```

Complete error handling is essential for building reliable and maintainable software.