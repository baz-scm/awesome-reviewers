---
title: "Handle protocol headers properly"
description: "When implementing network services, especially proxies and protocol handlers, proper HTTP header management is critical for correct functionality, compatibility, and diagnostics."
repository: "tokio-rs/axum"
label: "Networking"
language: "Rust"
comments_count: 4
repository_stars: 22100
---

When implementing network services, especially proxies and protocol handlers, proper HTTP header management is critical for correct functionality, compatibility, and diagnostics.

For proxy services:
- Remove or replace the `HOST` header when forwarding requests to avoid conflicts
- Include standard forwarded headers to maintain origin information:
  ```rust
  // Add standard proxy headers
  req.headers_mut().insert(
      "X-Forwarded-Host", 
      original_host.clone()
  );
  req.headers_mut().insert(
      "X-Forwarded-Proto",
      HeaderValue::from_static(original_scheme)
  );
  req.headers_mut().insert(
      "X-Forwarded-For",
      client_ip.to_string().parse().unwrap()
  );
  ```

For protocol upgrades (like WebSockets):
- Validate required headers with specific error messages
  ```rust
  let sec_websocket_key = req
      .headers_mut()
      .remove(header::SEC_WEBSOCKET_KEY)
      .ok_or(WebSocketKeyHeaderMissing)?;
  ```
- Be aware of protocol version differences (HTTP/1.0 doesn't support upgrades, HTTP/1.1 uses GET for WebSockets, later versions use CONNECT)
- Document the last points where protocol-specific data is available:
  ```rust
  /// This is the last point where we can extract TCP/IP metadata such as 
  /// IP address of the client as well as things from HTTP headers
  ```

Proper header handling improves interoperability, makes debugging easier, and creates more robust network applications.