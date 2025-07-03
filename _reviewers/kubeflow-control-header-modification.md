---
title: Control header modification
description: When allowing user-configurable HTTP headers in your application, implement
  strict validation to prevent security bypasses. Users should never be allowed to
  override security-critical headers that could compromise authentication or authorization
  mechanisms.
repository: kubeflow/kubeflow
label: Security
language: Go
comments_count: 1
repository_stars: 15064
---

When allowing user-configurable HTTP headers in your application, implement strict validation to prevent security bypasses. Users should never be allowed to override security-critical headers that could compromise authentication or authorization mechanisms.

Use a whitelist approach for maximum security:

```go
// Example: Whitelist approach for header validation
if _, ok := annotations["app.kubeflow.org/http-headers-request-set"]; ok {
    requestHeaders := strings.Split(annotations["app.kubeflow.org/http-headers-request-set"], "\n")
    for _, kv := range requestHeaders {
        if len(strings.Split(kv, ": ")) == 2 {
            k := strings.Split(kv, ": ")[0]
            v := strings.Split(kv, ": ")[1]
            
            // Only allow non-standard headers with X- prefix
            if strings.HasPrefix(k, "X-") {
                // Further validate against sensitive headers
                if !isRestrictedHeader(k) {
                    headers["request"].(map[string]interface{})["set"].(map[string]interface{})[k] = v
                }
            }
        }
    }
}
```

This prevents attackers from overriding critical headers like authentication tokens (e.g., `userid-header`), protocol information (e.g., `X-Forwarded-Proto`), or other security mechanisms. For applications with specific header requirements, maintain a carefully curated whitelist rather than allowing arbitrary header manipulation.
