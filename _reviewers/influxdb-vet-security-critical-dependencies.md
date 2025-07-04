---
title: Vet security-critical dependencies
description: 'When introducing new dependencies, especially those handling sensitive
  operations like language interpreters, perform comprehensive security due diligence
  before adoption. Evaluate each dependency against these security criteria:'
repository: influxdata/influxdb
label: Security
language: Toml
comments_count: 1
repository_stars: 30268
---

When introducing new dependencies, especially those handling sensitive operations like language interpreters, perform comprehensive security due diligence before adoption. Evaluate each dependency against these security criteria:

1. **Maintenance health**: Check for active development, large user base, and responsive contributors.
2. **Security track record**: Review CVE history to confirm security issues are promptly addressed.
3. **Security integration**: Verify integration with vulnerability tracking systems like GitHub advisories.
4. **Contingency planning**: Document alternatives if the dependency becomes unmaintained.

For critical dependencies, document your findings in a security assessment that includes:
- Vulnerability history analysis
- Update frequency and responsiveness
- Embedded component maintenance strategy (if applicable)
- Security monitoring approach

Example from assessment:
```rust
// Security-vetted dependency
[dependencies.pyo3]
version = "0.23.3"  // Includes fix for CVE-2024-9979
```

Always maintain awareness of dependency status. When a critical dependency becomes unmaintained (as happened with PyOxidizer), promptly implement your contingency plan by switching to maintained alternatives (like using pyo3 with python-build-standalone).