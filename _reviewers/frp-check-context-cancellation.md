---
title: Check context cancellation
description: 'Always implement proper cancellation mechanisms in concurrent code to
  prevent goroutine leaks and enable timely shutdown. Two key practices:


  1. Add context checks at the beginning of loops in goroutines:'
repository: fatedier/frp
label: Concurrency
language: Go
comments_count: 2
repository_stars: 95938
---

Always implement proper cancellation mechanisms in concurrent code to prevent goroutine leaks and enable timely shutdown. Two key practices:

1. Add context checks at the beginning of loops in goroutines:
```go
for {
    // Honor caller cancellation to avoid goroutine leaks
    select {
    case <-ctx.Done():
        logger.Debug("operation cancelled")
        return
    default:
    }
    
    // Continue with operation that might block
    data, err := ReadMessage(conn)
    // ...
}
```

2. Add context parameters to functions that may block for extended periods:
```go
// Before
func (impl *transporterImpl) Send(m msg.Message) error

// After
func (impl *transporterImpl) Send(ctx context.Context, m msg.Message) error
```

This pattern allows callers to cancel operations when a user exits manually or when operations exceed timeouts, preventing resource leaks and ensuring responsive application behavior during shutdown.