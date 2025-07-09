---
title: Harden CI/CD runners
description: All CI/CD workflow jobs must implement security controls for network
  traffic, particularly using the step-security/harden-runner action or equivalent
  technology. This prevents potential supply chain attacks or unauthorized data exfiltration
  during automated builds and tests.
repository: neondatabase/neon
label: Security
language: Yaml
comments_count: 1
repository_stars: 19015
---

All CI/CD workflow jobs must implement security controls for network traffic, particularly using the step-security/harden-runner action or equivalent technology. This prevents potential supply chain attacks or unauthorized data exfiltration during automated builds and tests.

Example:
```yml
- name: Harden the runner (Audit all outbound calls)
  uses: step-security/harden-runner@4d991eb9b905ef189e4c376166672c3f2f230481 # v2.11.0
  with:
    egress-policy: audit
```

Ensure this step is added consistently to all jobs in CI/CD workflows to maintain a strong security posture across the entire build pipeline.