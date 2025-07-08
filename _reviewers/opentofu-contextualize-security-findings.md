---
title: Contextualize security findings
description: When reporting security vulnerabilities, include sufficient context beyond
  just vulnerability IDs or codes. Always preserve standard identifiers (like GO-YYYY-NNNN)
  in titles while adding descriptive information about affected components, versions,
  and modules. This makes vulnerabilities easier to prioritize, track, and remediate.
repository: opentofu/opentofu
label: Security
language: Yaml
comments_count: 2
repository_stars: 25901
---

When reporting security vulnerabilities, include sufficient context beyond just vulnerability IDs or codes. Always preserve standard identifiers (like GO-YYYY-NNNN) in titles while adding descriptive information about affected components, versions, and modules. This makes vulnerabilities easier to prioritize, track, and remediate.

For example:
```
// Instead of just:
Issue: "GO-2024-1234 reported"

// Prefer:
Issue: "GO-2024-1234 reported - affects authentication module in v1.7-v1.9"
Description:
"This vulnerability is affecting the following versions: v1.7 v1.8 v1.9
*Vulnerability info:* https://pkg.go.dev/vuln/GO-2024-1234
*Pipeline run:* https://github.com/org/repo/actions/runs/12345
*Affected component:* authentication/oauth2"
```

Properly labeled and contextualized vulnerability reports allow teams to quickly understand the severity and impact without opening multiple tabs or digging through comments. Consider adding clear documentation on how to handle these vulnerabilities and restricting sensitive security discussions to appropriate team members when necessary.