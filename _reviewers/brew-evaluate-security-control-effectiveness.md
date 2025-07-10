---
title: Evaluate security control effectiveness
description: Security measures should be evaluated against realistic threat models
  to avoid creating a false sense of security. When implementing security controls
  like checksums, consider whether they actually protect against likely attack vectors.
repository: Homebrew/brew
label: Security
language: Markdown
comments_count: 1
repository_stars: 44168
---

Security measures should be evaluated against realistic threat models to avoid creating a false sense of security. When implementing security controls like checksums, consider whether they actually protect against likely attack vectors.

For example, in package management systems that download from third-party sources:

```
# INSUFFICIENT SECURITY:
# The sha256 verification provides limited protection if the attacker can control both:
# - The download URL source
# - Version information being reported

# Better approach: Implement defense-in-depth with multiple complementary security controls
# - Digital signatures from trusted authorities
# - Reproducible builds to verify package contents
# - Monitoring for unexpected behavior or changes
```

Remember that sophisticated attackers target the weakest links in your security chain. If they can compromise one control (like a download URL), they can often compromise related controls (like version reporting), rendering single verification methods inadequate.