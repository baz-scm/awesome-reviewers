---
title: Organize code logically
description: 'Maintain a clean and logical code structure by properly organizing code
  according to its functionality and purpose:


  1. Group related functionality into dedicated packages based on domain logic (e.g.,
  `pkg/ssh` for SSH-related code)'
repository: fatedier/frp
label: Code Style
language: Go
comments_count: 6
repository_stars: 95938
---

Maintain a clean and logical code structure by properly organizing code according to its functionality and purpose:

1. Group related functionality into dedicated packages based on domain logic (e.g., `pkg/ssh` for SSH-related code)
2. Keep static/asset files in separate directories rather than embedding them alongside application code
3. Follow Go's import convention with a single, organized import section that separates standard library and third-party imports
4. Structure complex patterns like multiple callbacks into interfaces and structs for better readability

Example of proper import organization:
```go
// Good: Organized import section
import (
    "context"
    "crypto/tls"
    "fmt"
    
    "github.com/fatedier/frp/models/transport"
)
```

Example of improving complex parameter patterns with structured types:
```go
// Before
func NewVhostMuxer(listener net.Listener, vhostFunc muxFunc, authFunc httpAuthFunc, 
                  successFunc successFunc, rewriteFunc hostRewriteFunc, timeout time.Duration) {
    // ...
}

// After
type MuxerOptions struct {
    VhostFunc   muxFunc
    AuthFunc    httpAuthFunc
    SuccessFunc successFunc
    RewriteFunc hostRewriteFunc
    Timeout     time.Duration
}

func NewVhostMuxer(listener net.Listener, options MuxerOptions) {
    // ...
}
```

This organization improves code maintainability, makes navigation easier for developers, and establishes a consistent project structure that scales with codebase growth.