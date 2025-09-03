---
title: Enforce secure TLS configuration
description: Always configure TLS connections with secure minimum version requirements
  and proper certificate handling. Network communications should enforce TLS 1.2 or
  higher to prevent security vulnerabilities from outdated protocols.
repository: gofiber/fiber
label: Networking
language: Go
comments_count: 3
repository_stars: 37560
---

Always configure TLS connections with secure minimum version requirements and proper certificate handling. Network communications should enforce TLS 1.2 or higher to prevent security vulnerabilities from outdated protocols.

When configuring TLS in clients or servers, explicitly set the minimum version and validate certificate configurations:

```go
// Server TLS configuration
tlsConfig := &tls.Config{
    MinVersion: tls.VersionTLS12, // Enforce TLS 1.2 minimum
}

// Client TLS configuration with certificates
func (c *Client) TLSConfig() *tls.Config {
    if c.tlsConfig == nil {
        c.tlsConfig = &tls.Config{
            MinVersion: tls.VersionTLS12,
        }
    }
    return c.tlsConfig
}
```

Additionally, ensure comprehensive testing of TLS compatibility scenarios, including cases where client and server have different TLS version requirements. Test handshake failures when version mismatches occur (e.g., server only allows TLS 1.3 but client attempts TLS 1.2). This prevents production issues and ensures robust network security across different deployment environments.