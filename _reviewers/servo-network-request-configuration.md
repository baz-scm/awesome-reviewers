---
title: Network request configuration
description: When creating network requests, ensure all security-sensitive parameters
  are properly configured including origin, referrer, CORS mode, and destination.
  Incomplete request configuration can lead to test failures, security vulnerabilities,
  and incorrect cross-origin behavior.
repository: servo/servo
label: Networking
language: Rust
comments_count: 2
repository_stars: 32962
---

When creating network requests, ensure all security-sensitive parameters are properly configured including origin, referrer, CORS mode, and destination. Incomplete request configuration can lead to test failures, security vulnerabilities, and incorrect cross-origin behavior.

Always specify:
- **Origin**: Set to the document's origin for the request context
- **Referrer**: Use the document URL rather than NoReferrer when appropriate  
- **CORS mode**: Configure based on the request type and cross-origin requirements
- **Destination**: Specify the correct destination type (e.g., Font, Script, etc.)

Example of proper request configuration:
```rust
let request = RequestBuilder::new(
    state.webview_id,
    url.clone().into(),
    Referrer::ReferrerUrl(document_context.document_url.clone()),
)
.destination(Destination::Font)
.mode(RequestMode::CorsMode)
.origin(ImmutableOrigin::new(url.origin()));
```

Be particularly careful with CORS mode settings as they can cause failures when loading cross-origin resources. Test thoroughly when modifying request builder parameters, as incomplete configuration often manifests as test failures that may not be immediately obvious.