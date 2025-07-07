---
title: Validate security-critical inputs
description: 'Always implement thorough validation for user-controllable inputs that
  could pose security risks. Particularly:


  1. **Path validation**: Protect against path traversal attacks by rejecting paths
  containing directory traversal sequences (`..`) or by resolving paths against a
  safe base directory.'
repository: fatedier/frp
label: Security
language: Go
comments_count: 2
repository_stars: 95938
---

Always implement thorough validation for user-controllable inputs that could pose security risks. Particularly:

1. **Path validation**: Protect against path traversal attacks by rejecting paths containing directory traversal sequences (`..`) or by resolving paths against a safe base directory.

2. **Domain/subdomain validation**: Validate domain-related inputs against potentially dangerous characters (like `.` or `*` in subdomains) that could be used for attacks.

Example for path validation:
```go
// Incorrect - vulnerable to path traversal
func (f *FileSource) Validate() error {
    if f.Path == "" {
        return errors.New("file path cannot be empty")
    }
    return nil
}

// Better - validates against path traversal attempts
func (f *FileSource) Validate() error {
    if f.Path == "" {
        return errors.New("file path cannot be empty")
    }
    if strings.Contains(f.Path, "..") {
        return errors.New("path cannot contain directory traversal sequences")
    }
    // Consider additional checks like absolute path resolution
    return nil
}
```

Failing to validate these inputs can lead to serious security vulnerabilities including unauthorized file access, server-side request forgery, or other injection-based attacks.