---
title: Obfuscate test secrets
description: Do not commit cryptographic material that looks like a real secret (private
  keys, signed certificates, passwords, tokens) into the repository in plain text,
  even when it is intentionally generated for tests (e.g., a "distrusted" or revoked
  test certificate/key). Automated secret scanners used by mirrors, CI systems, and
  security report pipelines cannot...
repository: python/cpython
label: Security
language: Other
comments_count: 1
repository_stars: 77696
---

Do not commit cryptographic material that looks like a real secret (private keys, signed certificates, passwords, tokens) into the repository in plain text, even when it is intentionally generated for tests (e.g., a "distrusted" or revoked test certificate/key). Automated secret scanners used by mirrors, CI systems, and security report pipelines cannot distinguish deliberately-invalid test credentials from leaked production secrets; this generates false "leaked key" reports, blocks pushes, and creates unnecessary security triage overhead for maintainers and downstream consumers.

When a test genuinely needs such material:
- Prefer generating it at runtime (e.g., via `openssl` key/cert generation) when the operation is cheap, rather than checking in static files.
- If static fixtures are required, store them in a form that defeats naive pattern/string scanning, such as an encrypted archive (e.g., a password-protected ZIP) rather than raw `.pem`/`.key` files with recognizable headers.
- Clearly name the artifacts to indicate their purpose (e.g., prefix with `distrusted_`) so humans reviewing scanner alerts can quickly confirm these are intentionally invalid/test-only credentials.

Example: instead of checking in `distrusted_intermediate.key` and `distrusted_keycert.pem` as plain PEM files, package them into an encrypted ZIP (e.g., `certdata.zip`) that tests extract on demand, avoiding trivial grep-based detection while still keeping the fixtures available for testing.