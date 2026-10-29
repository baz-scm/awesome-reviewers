---
title: Secure sensitive data handling
description: 'When implementing security-sensitive features (parsing untrusted cryptographic
  configs, enforcing TLS role restrictions, or maintaining a distrust/pinning list),
  apply defense-in-depth rather than relying on incidental implementation details:'
repository: python/cpython
label: Security
language: C
comments_count: 6
repository_stars: 77696
---

When implementing security-sensitive features (parsing untrusted cryptographic configs, enforcing TLS role restrictions, or maintaining a distrust/pinning list), apply defense-in-depth rather than relying on incidental implementation details:

1. Validate untrusted/external input against the intended security semantics, not against whatever internal error code a library happens to raise. If skip-vs-reject logic depends on a specific OpenSSL error reason, document it as a stopgap, add tests pinning each failure mode, and prefer a documented library API or explicit parsing when available. Don't silently accept alternate encodings (e.g. base64) unless that is the intended, documented behavior.

2. Enforce authorization/role checks consistently at every entry point that touches the sensitive operation, not just the most visible one. For example, if a client-only SSL feature is rejected on the socket, the corresponding context-level setter/getter must apply the same role check (`PROTOCOL_TLS_CLIENT`/`PROTOCOL_TLS_SERVER`) so a misconfigured context can't silently do the wrong thing. Never land a new security-relevant API endpoint without the same guards, documentation, and tests as its siblings.

3. Store and compare sensitive cryptographic material (keys, pinned/distrusted fingerprints) using well-defined, non-reversible representations rather than embedding raw key material: hash it (e.g. SHA-256 of the SPKI, as Go/Chrome CRLSet do) instead of storing raw DER, both to avoid leaking sensitive byte patterns into the binary and to keep comparisons fixed-size and constant-time where feasible.

4. When comparing fixed-size security values, use an explicit, named length constant (e.g. `SHA256_DIGEST_LENGTH`) instead of `sizeof(array_element)`; `sizeof` on a struct/array member is fragile against future type changes and can silently shrink the comparison window, weakening the security guarantee. Pair this with an assertion that the stored data size matches the expected digest length to fail loudly rather than silently truncating comparisons.

Example:
```c
/* store SHA-256 digest, not raw SPKI DER */
unsigned char digest[EVP_MAX_MD_SIZE];
unsigned int digest_len = 0;
EVP_Digest(spki, spki_len, digest, &digest_len, EVP_sha256(), NULL);
assert(digest_len == SHA256_DIGEST_LENGTH);
for (size_t i = 0; i < Py_ARRAY_LENGTH(_distrusted_spki); i++) {
    if (memcmp(digest, _distrusted_spki[i], SHA256_DIGEST_LENGTH) == 0) {
        return 1; /* distrusted */
    }
}
```