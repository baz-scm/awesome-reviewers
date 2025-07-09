---
title: Secure authentication handling
description: 'Always implement proper authentication checks and protect sensitive
  credentials throughout your codebase. This includes:


  1. **Validate all authentication inputs properly** to prevent panics and security
  vulnerabilities:'
repository: neondatabase/neon
label: Security
language: Rust
comments_count: 3
repository_stars: 19015
---

Always implement proper authentication checks and protect sensitive credentials throughout your codebase. This includes:

1. **Validate all authentication inputs properly** to prevent panics and security vulnerabilities:
```rust
// Bad: Will panic on short inputs
if &authorization[0..7] != "Bearer " {
    // ...
}

// Good: Safe parsing without panic risk
if let Some(token) = authorization.strip_prefix("Bearer ") {
    // Process token safely
} else {
    return Err(tonic::Status::invalid_argument("invalid authorization format"));
}
```

2. **Implement permission checks for all API endpoints**, even internal or testing ones:
```rust
// Always add permission checks to new endpoints
async fn your_api_endpoint(
    request: Request<Body>,
    _cancel: CancellationToken,
) -> Result<Response<Body>, ApiError> {
    // Add this check to prevent unauthorized access
    check_permissions(&request, None)?;
    
    // Rest of your endpoint logic
    // ...
}
```

3. **Redact sensitive information in logs** to prevent credential exposure:
```rust
// When logging URLs or other structures that might contain credentials
match url::Url::parse(url) {
    Ok(mut url) => {
        if url.password().is_some() {
            let _ = url.set_password(Some("_redacted_"));
        }
        // Now safe to log
        info!("Using URL: {}", url);
    }
    // ...
}
```

These practices prevent unauthorized access to sensitive endpoints, reduce risks of credential leakage, and improve the overall security posture of the system.