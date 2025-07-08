---
title: Fix dependency vulnerabilities
description: 'Security vulnerabilities in dependencies must be addressed immediately
  rather than bypassed with flags like `--no-verify`. When security scans identify
  vulnerabilities in libraries like the one detected in pyjwt:'
repository: prowler-cloud/prowler
label: Security
language: Yaml
comments_count: 1
repository_stars: 11834
---

Security vulnerabilities in dependencies must be addressed immediately rather than bypassed with flags like `--no-verify`. When security scans identify vulnerabilities in libraries like the one detected in pyjwt:

```
VULNERABILITIES REPORTED
Vulnerability found in pyjwt version 2.9.0
Vulnerability ID: 74429
Affected spec: <2.10.1
ADVISORY: Affected versions of pyjwt are vulnerable to Partial
Comparison (CWE-187). This flaw allows attackers to bypass issuer (iss)...
CVE-2024-53861
```

Prioritize updating to a secure version before continuing development. Create a dedicated PR to address the vulnerability rather than working around security checks. For critical security issues, establish a policy that prevents merging code with known high-severity vulnerabilities and define clear remediation timeframes based on severity levels.