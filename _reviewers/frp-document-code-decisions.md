---
title: Document code decisions
description: Always include clear documentation for important code decisions and metadata.
  This includes preserving copyright notices and explaining the reasoning behind specific
  values and constants.
repository: fatedier/frp
label: Documentation
language: Go
comments_count: 2
repository_stars: 95938
---

Always include clear documentation for important code decisions and metadata. This includes preserving copyright notices and explaining the reasoning behind specific values and constants.

For copyright notices:
- Maintain all original copyright information
- Add new copyright notices on separate lines, never replacing existing ones

For code constants and values:
- Replace hard-coded "magic numbers" with named constants
- Add comments explaining the reasoning behind specific values, especially for timeouts, limits, and other non-obvious choices

Example:
```go
// Original hard-coded value
svr.rc.VhostTcpMuxer, err = vhost.NewTcpHttpTunnelMuxer(l, 30*time.Second)

// Improved version with named constant and explanation
// DefaultTunnelTimeout defines how long to wait before closing inactive connections
// 30 seconds was chosen based on average connection usage patterns
const DefaultTunnelTimeout = 30 * time.Second
svr.rc.VhostTcpMuxer, err = vhost.NewTcpHttpTunnelMuxer(l, DefaultTunnelTimeout)
```