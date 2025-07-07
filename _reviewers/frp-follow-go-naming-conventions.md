---
title: Follow Go naming conventions
description: "Adhere to Go's standard naming conventions for identifiers:\n\n1. **Control\
  \ visibility with capitalization**:\n   - Use uppercase first letter for exported\
  \ (public) identifiers"
repository: fatedier/frp
label: Naming Conventions
language: Go
comments_count: 4
repository_stars: 95938
---

Adhere to Go's standard naming conventions for identifiers:

1. **Control visibility with capitalization**:
   - Use uppercase first letter for exported (public) identifiers
   - Use lowercase first letter for unexported (package-private) identifiers
   - Only export what needs to be used outside the package

2. **Capitalize acronyms properly**:
   - Write acronyms in all caps (e.g., `HTTP`, `TCP`, `TLS`, not `Http`, `Tcp`, `Tls`)
   - Apply this to all identifiers (variables, functions, types, etc.)

Example of improper naming:
```go
type TcpHttpTunnelProxy struct {
    // ...
}

var ResponseHeaderTimeout int64
var TlsVerify bool

type BaseAuth struct {
    // Not needed outside package
}
```

Example of proper naming:
```go
type TCPHTTPTunnelProxy struct {
    // ...
}

var responseHeaderTimeout int64
var TLSVerify bool

type baseAuth struct {
    // Not exported as it's only used within the package
}
```

Following these conventions improves code readability, maintains consistency with standard Go code, and makes the public API of your package more obvious.