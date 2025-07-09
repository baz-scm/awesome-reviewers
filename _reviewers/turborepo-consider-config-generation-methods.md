---
title: Consider config generation methods
description: When implementing code to handle configuration files like lockfiles or
  environment settings, carefully consider the trade-offs between direct serialization
  and template-based approaches. While direct serialization from data structures is
  often simpler and less error-prone, template-based generation may provide better
  control over formatting, whitespace...
repository: vercel/turborepo
label: Configurations
language: Go
comments_count: 2
repository_stars: 28115
---

When implementing code to handle configuration files like lockfiles or environment settings, carefully consider the trade-offs between direct serialization and template-based approaches. While direct serialization from data structures is often simpler and less error-prone, template-based generation may provide better control over formatting, whitespace sensitivity, and diffing capabilities. Document your reasoning when choosing an approach, especially when standard libraries have limitations (such as the Go YAML package's limited whitespace control). Consider how the consuming tools will interpret the generated files and whether preservation of specific formatting is important for your use case.

Example:
```go
// Template-based approach for better whitespace control
const pnpmLockfileTemplate = `lockfileVersion: {{ .Version }}

importers:
{{ range $key, $val := .Importers }}
  {{ $key }}:
{{ displayProjectSnapshot $val }}
{{ end }}
packages:
{{ range $key, $val :=  .Packages }}
  {{ $key }}:
{{ displayPackageSnapshot $val }}
{{ end }}{{ if (eq .Version 5.4) }}
{{ end }}`
```