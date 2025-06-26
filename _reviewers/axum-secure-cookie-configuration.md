---
title: "Secure cookie configuration"
description: "Always set appropriate security flags on cookies, especially those used for authentication or session management. At minimum, include HttpOnly, Secure, and SameSite flags to prevent cookie theft, session hijacking, and cross-site request forgery attacks."
repository: "tokio-rs/axum"
label: "Security"
language: "Rust"
comments_count: 1
repository_stars: 22100
---

Always set appropriate security flags on cookies, especially those used for authentication or session management. At minimum, include:

1. `HttpOnly` - Prevents JavaScript access to the cookie, protecting against XSS attacks
2. `Secure` - Ensures the cookie is only sent over HTTPS connections
3. `SameSite` - Use `Lax` for cookies needed after redirects (like OAuth flows), or `Strict` for maximum protection when redirects aren't needed

Example of properly configured cookie in an OAuth flow:

```rust
// Attach the session cookie to the response header with security flags
let cookie = format!(
    "{COOKIE_NAME}={cookie}; SameSite=Lax; Path=/; HttpOnly; Secure"
);
```

These settings significantly reduce the risk of cookie theft, session hijacking, and cross-site request forgery attacks.