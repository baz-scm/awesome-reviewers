---
title: Explain complex logic
description: Add explanatory comments for non-obvious code sections, complex business
  logic, and public methods to clarify their purpose and reasoning. Comments should
  explain the "why" behind decisions and the "what" for functions that aren't immediately
  clear from their implementation.
repository: snyk/cli
label: Documentation
language: Go
comments_count: 2
repository_stars: 5178
---

Add explanatory comments for non-obvious code sections, complex business logic, and public methods to clarify their purpose and reasoning. Comments should explain the "why" behind decisions and the "what" for functions that aren't immediately clear from their implementation.

For conditional logic with business rules, explain the rationale:
```go
// Cobra has its own help mechanism, however since we have help documentation 
// only in legacy CLI, we should fallback to calling it for flag errors
if commandError {
    resultError = handleErrorFallbackToLegacyCLI
} else if flagError {
    resultError = handleErrorShowHelp
}
```

For public methods, provide high-level documentation describing what the method does:
```go
// ConnectToProxy establishes a connection to the specified proxy server
// and handles the authentication handshake for the target address
func (p *ProxyAuthenticator) ConnectToProxy(ctx context.Context, proxyURL *url.URL, target string, connection net.Conn) error {
```

Focus on areas where the code's intent or business logic isn't immediately apparent to future maintainers.