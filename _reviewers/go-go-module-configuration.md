---
title: Go module configuration
description: Ensure Go projects use modern module configuration instead of legacy
  GOPATH setup. Projects should be created outside of GOPATH directory structure,
  with proper environment variable configuration and module files.
repository: golang/go
label: Configurations
language: Html
comments_count: 3
repository_stars: 129599
---

Ensure Go projects use modern module configuration instead of legacy GOPATH setup. Projects should be created outside of GOPATH directory structure, with proper environment variable configuration and module files.

Key requirements:
- Set GO111MODULE=on environment variable when using Go 1.11 (redundant in Go 1.12+)
- Create projects in user-friendly locations (~/myproject/, Desktop, Documents) rather than $GOPATH/src/
- Always include go.mod file in project root via `go mod init`
- Avoid github.com/user placeholder paths in documentation

Example project structure:
```
~/myproject/
    hello/
        go.mod        # module file
        hello.go      # command source
        stringutil/
            reverse.go # package source
```

This approach eliminates GOPATH dependency, simplifies project setup, and aligns with modern Go development practices. The configuration ensures compatibility across different Go versions while providing a cleaner development experience.