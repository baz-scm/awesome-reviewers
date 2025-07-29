---
title: explicit cryptographic parameters
description: Always explicitly specify security-critical parameters in cryptographic
  operations rather than relying on default values. This prevents vulnerabilities
  that could arise from misunderstood defaults or future changes to default behavior.
repository: vlang/v
label: Security
language: Markdown
comments_count: 1
repository_stars: 36582
---

Always explicitly specify security-critical parameters in cryptographic operations rather than relying on default values. This prevents vulnerabilities that could arise from misunderstood defaults or future changes to default behavior.

When working with cryptographic APIs, be explicit about hash algorithms, key sizes, padding schemes, and other security-relevant configurations. This makes the security intent clear and protects against breaking changes to library defaults.

Example of what to avoid:
```v
// Unclear what hash algorithm is being used
signature := pvkey.sign(message_tobe_signed)!
```

Example of preferred approach:
```v
// Explicitly specify the hash configuration
signature := pvkey.sign(message_tobe_signed, hash_config: .with_recommended_hash)!
```

This practice is especially important when there's uncertainty about what the default behavior actually is, as defaults in security libraries can change between versions or may not be what developers expect.