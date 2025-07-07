---
title: Validate with sensible defaults
description: Implement a comprehensive configuration validation strategy that combines
  centralized validation functions with appropriate default values and user-friendly
  messaging. Instead of failing with errors on non-critical configuration issues,
  provide warnings and continue with sensible defaults.
repository: fatedier/frp
label: Configurations
language: Go
comments_count: 4
repository_stars: 95938
---

Implement a comprehensive configuration validation strategy that combines centralized validation functions with appropriate default values and user-friendly messaging. Instead of failing with errors on non-critical configuration issues, provide warnings and continue with sensible defaults.

**Key practices:**

1. Move configuration validation to dedicated check functions (like `CheckForCli` and `CheckForSvr`)
2. Provide sensible defaults for optional configuration values rather than requiring them all
3. Use warnings instead of errors for non-critical configuration issues
4. Centralize validation logic to support multiple configuration formats

**Example:**

```go
// Bad practice - returning error for non-critical configuration issue
if cfg.TLSEnable == false && cfg.TLSCertFile != "" {
    return fmt.Errorf("Parse conf error: forbidden tls_cert_file, it only works when tls_enabled is true")
}

// Good practice - providing warning for non-critical configuration issue
if cfg.TLSEnable == false {
    if cfg.TLSCertFile != "" {
        fmt.Println("WARNING! tls_cert_file is invalid when tls_enable is false")
    }
}

// Bad practice - requiring all configuration values
proxyClient.LocalIp, ok = section["local_ip"]
if !ok {
    return fmt.Errorf("Parse ini file error: proxy [%s] no local_ip found", proxyClient.Name)
}

// Good practice - providing sensible default
if localIP, ok := section["local_ip"]; ok {
    proxyClient.LocalIp = localIP
} else {
    proxyClient.LocalIp = "127.0.0.1" // Sensible default
}
```

This approach improves user experience by allowing applications to start with reasonable defaults while clearly communicating configuration issues. It also facilitates future changes by centralizing validation logic rather than scattering it throughout the codebase.