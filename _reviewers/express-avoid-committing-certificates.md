---
title: Avoid committing certificates
description: Never commit SSL/TLS certificates, private keys, or other generated cryptographic
  material into the repository. These artifacts expire, can leak sensitive key material,
  and quickly become stale or invalid. Instead, exclude them via .gitignore and provide
  a script or documented steps (e.g., in README.md) for generating them locally, optionally
  referencing an...
repository: Expressjs/Express
label: Security
language: Other
comments_count: 1
repository_stars: 69580
---

Never commit SSL/TLS certificates, private keys, or other generated cryptographic material into the repository. These artifacts expire, can leak sensitive key material, and quickly become stale or invalid. Instead, exclude them via .gitignore and provide a script or documented steps (e.g., in README.md) for generating them locally, optionally referencing an npm module or openssl command that auto-generates fresh certs. For example, replace a checked-in cert.pem with instructions like:

```bash
# README.md
## Generating a self-signed certificate for this example
openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 365
```

This keeps examples secure, always up to date, and avoids accidentally distributing expired or compromised credentials.