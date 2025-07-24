---
title: Validate untrusted inputs
description: Always validate and sanitize user-provided inputs to prevent injection
  attacks, particularly path traversal vulnerabilities. User inputs should be treated
  as untrusted and validated against expected patterns before use in file operations,
  URL construction, or system commands.
repository: argoproj/argo-cd
label: Security
language: Go
comments_count: 4
repository_stars: 20149
---

Always validate and sanitize user-provided inputs to prevent injection attacks, particularly path traversal vulnerabilities. User inputs should be treated as untrusted and validated against expected patterns before use in file operations, URL construction, or system commands.

Key areas requiring validation:
- **Path construction**: Validate repository names, chart names, and versions to prevent directory traversal attacks like `../../../etc/passwd`
- **File path operations**: Use secure path joining methods (like `securejoin`) when dealing with user-provided paths that could contain symlinks or relative path components
- **Resource access**: Implement proper access controls for cross-namespace resource access, requiring explicit labels or permissions rather than allowing arbitrary access
- **Executable paths**: Avoid relative paths in PATH lookups that could enable current directory exploits; use absolute paths and validate executable locations

Example of vulnerable code:
```go
// Vulnerable - no validation
args = append(args, fmt.Sprintf("%s/%s-%s.tgz", repo, chartName, version))

// Better - with validation
if !isValidRepoName(repo) || !isValidChartName(chartName) || !isValidVersion(version) {
    return "", fmt.Errorf("invalid input parameters")
}
args = append(args, fmt.Sprintf("%s/%s-%s.tgz", repo, chartName, version))
```

Implement input validation early in the request processing pipeline and use allowlists rather than denylists when possible. Consider using established validation libraries rather than implementing custom validation logic.