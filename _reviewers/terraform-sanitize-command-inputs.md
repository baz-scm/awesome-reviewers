---
title: Sanitize command inputs
description: When constructing commands that will be executed, always sanitize input
  values to prevent command injection vulnerabilities. Never directly substitute user-supplied
  or externally-sourced data into command strings without proper validation and sanitization.
repository: hashicorp/terraform
label: Security
language: Go
comments_count: 1
repository_stars: 45532
---

When constructing commands that will be executed, always sanitize input values to prevent command injection vulnerabilities. Never directly substitute user-supplied or externally-sourced data into command strings without proper validation and sanitization.

Unsafe pattern (vulnerable to injection):
```go
command := strings.Replace(proxyCommand, "%h", host, -1)
// Executing this command could be dangerous if 'host' contains malicious characters
```

Safer alternatives:
1. Validate inputs against strict patterns before use
```go
if !validHostnamePattern.MatchString(host) {
    return nil, fmt.Errorf("Invalid hostname format: %s", host)
}
```

2. Use dedicated libraries/APIs that handle command arguments safely
```go
cmd := exec.Command(proxyCommand, host, port)
// Arguments are properly escaped by the exec package
```

3. If string interpolation is necessary, consider using a dedicated escaping function
```go
escapedHost := shellEscape(host)
command := strings.Replace(proxyCommand, "%h", escapedHost, -1)
```

This practice helps protect against attackers who might craft malicious input to execute unauthorized commands on your system.