---
title: Document security behavior references
description: When implementing security-related functionality such as certificate
  parsing, cryptographic validation, or authentication mechanisms, always document
  the expected behavior and include references to official documentation that explains
  the underlying security decisions.
repository: istio/istio
label: Security
language: Other
comments_count: 1
repository_stars: 37192
---

When implementing security-related functionality such as certificate parsing, cryptographic validation, or authentication mechanisms, always document the expected behavior and include references to official documentation that explains the underlying security decisions.

This practice is crucial for several reasons:
- It helps future maintainers understand why certain security behaviors exist
- It provides authoritative backing for security decisions during audits
- It ensures that security implementations align with established standards and best practices
- It makes debugging easier when security-related failures occur

Example:
```go
// This cert has a negative serial number.
// Go should fail to parse it, but we should handle this gracefully
// Reference: https://golang.org/pkg/crypto/x509/#Certificate
// Go's x509 package rejects certificates with negative serial numbers
// as per RFC 5280 requirements
```

Always include links to relevant RFCs, official language documentation, or security standards when implementing security features. This documentation becomes invaluable during security reviews and helps establish the rationale behind security-related code decisions.