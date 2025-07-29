---
title: validate file paths
description: Always validate and sanitize file paths when processing external input
  to prevent directory traversal attacks, zip slip vulnerabilities, and other path-based
  security issues. Check for minimum required path components, reject paths with suspicious
  patterns, and ensure paths stay within expected boundaries.
repository: traefik/traefik
label: Security
language: Go
comments_count: 1
repository_stars: 55772
---

Always validate and sanitize file paths when processing external input to prevent directory traversal attacks, zip slip vulnerabilities, and other path-based security issues. Check for minimum required path components, reject paths with suspicious patterns, and ensure paths stay within expected boundaries.

Example from zip extraction:
```go
// Split to discard the first part of the path, which is [organization]-[project]-[release commit sha1] when the archive is a Yaegi go plugin with vendoring.
pathParts := strings.SplitN(f.Name, "/", 2)
if len(pathParts) < 2 {
    return fmt.Errorf("no root directory: %s", f.Name)
}

// Validate and sanitize the file path
p := filepath.Join(dest, pathParts[1])
```

This pattern should be applied whenever processing file paths from archives, user uploads, API requests, or any external source where malicious paths could be injected.