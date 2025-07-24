---
title: Follow Go naming conventions
description: Adhere to Go naming conventions and maintain consistency with established
  codebase terminology. This includes proper capitalization of acronyms (e.g., "OCI"
  not "Oci"), avoiding underscores in identifiers, following standard library naming
  patterns, and using consistent terminology throughout the codebase.
repository: argoproj/argo-cd
label: Naming Conventions
language: Go
comments_count: 5
repository_stars: 20149
---

Adhere to Go naming conventions and maintain consistency with established codebase terminology. This includes proper capitalization of acronyms (e.g., "OCI" not "Oci"), avoiding underscores in identifiers, following standard library naming patterns, and using consistent terminology throughout the codebase.

Key guidelines:
- Capitalize acronyms properly: `GetOCICreds()` not `GetOciCreds()`
- Avoid underscores in Go names as flagged by golangci-lint
- Follow standard library patterns: `unmarshalYamlFile` not `unMarshalYamlFile` (consistent with `json.Unmarshal`)
- Use consistent terminology: prefer `APIVersion` over `groupVersion` when it aligns with backend terminology
- Add conventional suffixes where expected: timestamp gauges should include `_seconds` suffix

Example:
```go
// Good - follows Go conventions
func (repo *Repository) GetOCICreds() oci.Creds {
    // implementation
}

// Bad - incorrect acronym capitalization  
func (repo *Repository) GetOciCreds() oci.Creds {
    // implementation
}
```

Consistent naming reduces cognitive load, improves code readability, and aligns with community expectations and tooling requirements.