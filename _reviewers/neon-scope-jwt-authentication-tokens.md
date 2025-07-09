---
title: Scope JWT authentication tokens
description: 'Always include tenant, timeline, and endpoint identifiers in JWT tokens
  used for service authentication. This ensures proper isolation between tenants and
  prevents unauthorized access across endpoints or timelines, even within the same
  tenant hierarchy. '
repository: neondatabase/neon
label: Security
language: Markdown
comments_count: 4
repository_stars: 19015
---

Always include tenant, timeline, and endpoint identifiers in JWT tokens used for service authentication. This ensures proper isolation between tenants and prevents unauthorized access across endpoints or timelines, even within the same tenant hierarchy. 

Without proper token scoping, services cannot validate that requests come from authorized sources with the correct endpoint_id, creating potential security vulnerabilities where one endpoint could access another endpoint's data.

Implementation guidelines:
1. Control plane should generate fully-scoped JWT tokens
2. Include endpoint_id, tenant_id, and timeline_id in token claims
3. Use structured paths in storage that correspond to these identifiers
4. Services should validate all relevant identifiers before granting access

Example token generation:
```rust
// INSECURE: Token lacks proper scope
let token = generate_jwt_token(claims! {
    "tenant_id": tenant_id,
    // Missing endpoint and timeline identifiers!
});

// SECURE: Token includes all necessary identifiers
let token = generate_jwt_token(claims! {
    "tenant_id": tenant_id,
    "timeline_id": timeline_id,
    "endpoint_id": endpoint_id,
    "exp": expiration_time
});
```

Example path structure for storage access:
```
s3://<bucket>/tenant-<tenant_id>/tl-<timeline_id>/<endpoint_id>/
```

This approach protects against cross-tenant and cross-timeline attacks, as services can validate that requesters can only access resources matching their token scope.