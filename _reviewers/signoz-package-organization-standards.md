---
title: Package organization standards
description: Maintain proper package organization by following established structural
  patterns and separation of concerns. Code should be organized into appropriate packages
  based on functionality and responsibility.
repository: SigNoz/signoz
label: Code Style
language: Go
comments_count: 7
repository_stars: 23369
---

Maintain proper package organization by following established structural patterns and separation of concerns. Code should be organized into appropriate packages based on functionality and responsibility.

Key organizational principles:
1. **Module placement**: Business logic modules belong in `pkg/modules/`, not in `integrations/` or other generic folders
2. **Type definitions**: Data structures and domain types should be placed in `pkg/types/` with appropriate sub-packages (e.g., `cachetypes`, `quickfiltertypes`)
3. **Interface separation**: Follow the three-package rule - interface declarations, implementations, and mocks must be in separate packages to avoid circular dependencies
4. **Constructor patterns**: Complex object creation logic should be encapsulated in `New` functions within the types package
5. **Visibility control**: Only export types and functions that need to be used outside the package

Example of proper organization:
```go
// pkg/types/tracefunnel/tracefunnel.go - Type definitions
type Funnel struct { ... }

// pkg/modules/tracefunnel/module.go - Interface declaration  
type Module interface { ... }

// pkg/modules/tracefunnel/impltracefunnel/module.go - Implementation
type module struct { ... }

// pkg/modules/tracefunnel/tracefunneltest/mocks.go - Test mocks
type MockModule struct { ... }
```

This organization improves code maintainability, prevents circular dependencies, and makes the codebase more navigable for developers.