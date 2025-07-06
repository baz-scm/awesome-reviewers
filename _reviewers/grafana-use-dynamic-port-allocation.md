---
title: Use dynamic port allocation
description: When writing tests that require network services (HTTP, gRPC, or custom
  protocols), use port 0 to let the operating system assign available ports rather
  than hard-coding specific port numbers. Hard-coded ports can cause conflicts when
  multiple tests run simultaneously, leading to flaky tests.
repository: grafana/grafana
label: Networking
language: Go
comments_count: 2
repository_stars: 68825
---

When writing tests that require network services (HTTP, gRPC, or custom protocols), use port 0 to let the operating system assign available ports rather than hard-coding specific port numbers. Hard-coded ports can cause conflicts when multiple tests run simultaneously, leading to flaky tests.

After binding to the dynamic port, query the listener to determine which port was assigned for subsequent connection attempts:

```go
// Instead of this:
cfg.HTTPPort = "13000"
cfg.GRPCServer.Address = "127.0.0.1:20000"

// Do this:
listener, err := net.Listen("tcp", "127.0.0.1:0")
require.NoError(t, err)
port := listener.Addr().(*net.TCPAddr).Port
cfg.HTTPPort = strconv.Itoa(port)

// And for gRPC:
grpcListener, err := net.Listen("tcp", "127.0.0.1:0")
require.NoError(t, err)
grpcPort := grpcListener.Addr().(*net.TCPAddr).Port
cfg.GRPCServer.Address = fmt.Sprintf("127.0.0.1:%d", grpcPort)
```

This approach ensures tests are resilient to parallel execution and prevents port conflicts in CI environments where multiple builds might run concurrently.