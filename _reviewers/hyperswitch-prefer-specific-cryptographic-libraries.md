---
title: prefer specific cryptographic libraries
description: When adding cryptographic dependencies, critically evaluate whether broad
  libraries like OpenSSL are necessary or if more specific, focused alternatives can
  meet your requirements. Broad cryptographic libraries often include extensive functionality
  that may not be needed, potentially increasing the attack surface and complexity.
repository: juspay/hyperswitch
label: Security
language: Toml
comments_count: 1
repository_stars: 34028
---

When adding cryptographic dependencies, critically evaluate whether broad libraries like OpenSSL are necessary or if more specific, focused alternatives can meet your requirements. Broad cryptographic libraries often include extensive functionality that may not be needed, potentially increasing the attack surface and complexity.

Before adding general-purpose cryptographic libraries, consider:
- Whether a specific library (like RSA for RSA operations) can fulfill your needs
- The principle of least privilege - only include what you actually need
- Maintenance and security update considerations for smaller, focused libraries

Example from the codebase:
```toml
# Instead of:
openssl = "0.10"

# Consider using:
rsa = "0.9"  # If you only need RSA functionality
```

This approach reduces dependency bloat, minimizes potential security vulnerabilities, and makes your cryptographic intentions more explicit in the codebase.