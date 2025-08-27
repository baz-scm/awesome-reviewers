---
title: Secure configuration practices
description: 'Implement secure configuration practices to protect sensitive data and
  prevent security vulnerabilities. This includes three key areas:


  1. **Credential Protection**: Never store or transmit passwords and sensitive credentials
  in plain text. Use encryption tools, secure credential management systems, or environment
  variables with proper access controls.'
repository: volcano-sh/volcano
label: Security
language: Go
comments_count: 3
repository_stars: 4899
---

Implement secure configuration practices to protect sensitive data and prevent security vulnerabilities. This includes three key areas:

1. **Credential Protection**: Never store or transmit passwords and sensitive credentials in plain text. Use encryption tools, secure credential management systems, or environment variables with proper access controls.

2. **Authentication Handling**: When multiple authentication methods are supported, implement clear precedence rules to prevent conflicts and failures. For example, if both basic auth and token auth are configured, prioritize one method and clear the other to avoid authentication errors.

3. **Secure Defaults**: Disable debug endpoints, profiling tools, and other potentially sensitive features by default. Require explicit opt-in through configuration flags to enable these features.

Example of secure authentication handling:
```go
tConf := &transport.Config{
    Username:        p.conf["username"],
    Password:        p.conf["password"], 
    BearerToken:     p.conf["bearertoken"],
}
// If basic auth is set, token will be cleared to avoid conflicts
if tConf.Username != "" && tConf.Password != "" {
    tConf.BearerToken = ""
    tConf.BearerTokenFile = ""
}
```

Example of secure defaults:
```go
fs.BoolVar(&s.EnablePprof, "enable-pprof", false, "Enable the pprof endpoint; it is false by default")
```

These practices help prevent security audit issues, reduce attack surface, and ensure that sensitive functionality requires deliberate activation rather than accidental exposure.