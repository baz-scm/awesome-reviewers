---
title: Minimize credential data exposure
description: When handling security credentials (particularly TLS certificates) in
  data structures intended for transmission or serialization, include only the minimum
  necessary identifying information. Avoid passing complete certificate chains or
  redundant fields that have already been validated upstream.
repository: temporalio/temporal
label: Security
language: Go
comments_count: 1
repository_stars: 14953
---

When handling security credentials (particularly TLS certificates) in data structures intended for transmission or serialization, include only the minimum necessary identifying information. Avoid passing complete certificate chains or redundant fields that have already been validated upstream.

Instead of including entire certificate structures with all their fields:
```go
type AuthInfo struct {
    // Don't include these large fields
    // TLSConnection.State.PeerCertificates []x509.Certificate
    // TLSConnection.State.VerifiedChains [][]x509.Certificate
    
    // Instead, extract only essential identifying information
    FQDN       string `json:"fqdn,omitempty"`
    Fingerprint string `json:"fingerprint,omitempty"`
    CommonName string `json:"commonName,omitempty"`
}
```

This approach reduces payload size, improves performance, and follows the principle of least exposure for sensitive security information. When designing security-related data structures, always ask whether each field is truly necessary for the downstream consumer.