---
title: No committed certificates or secrets
description: Never check SSL/TLS certificates, private keys, tokens, or other security-sensitive
  credentials into version control, even in examples or test fixtures. Certificates
  expire and committed ones quickly become stale or invalid, and storing any cryptographic
  material in a repo creates unnecessary security risk and encourages bad habits.
  Instead, generate these...
repository: expressjs/Express
label: Security
language: Other
comments_count: 1
repository_stars: 69579
---

Never check SSL/TLS certificates, private keys, tokens, or other security-sensitive credentials into version control, even in examples or test fixtures. Certificates expire and committed ones quickly become stale or invalid, and storing any cryptographic material in a repo creates unnecessary security risk and encourages bad habits. Instead, generate these artifacts on demand: provide a script or an npm module that auto-generates the certificate/key pair during setup, or document clear steps in the README for users to generate their own locally. For example, replace a checked-in `cert.pem`/`key.pem` with a `README.md` snippet such as:

```bash
# Generate a self-signed certificate for local testing
openssl req -nodes -new -x509 -keyout key.pem -out cert.pem
```

This keeps the repository free of expiring or sensitive artifacts while still letting developers reproduce the required setup.