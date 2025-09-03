---
title: Configuration opt-in safety
description: When introducing new configuration options or making changes that could
  be disruptive, make them opt-in by default rather than enabled automatically. This
  prevents breaking existing functionality and gives users control over when to adopt
  new behaviors.
repository: angular/angular
label: Configurations
language: TypeScript
comments_count: 4
repository_stars: 98611
---

When introducing new configuration options or making changes that could be disruptive, make them opt-in by default rather than enabled automatically. This prevents breaking existing functionality and gives users control over when to adopt new behaviors.

Key principles:
- New features should be disabled by default with explicit flags to enable them
- Potentially disruptive migrations should require explicit opt-in
- Breaking configuration changes should be avoided, or made opt-in with clear migration paths
- Validate configuration options and provide clear error messages for unsupported settings

Example from migration configuration:
```typescript
// Bad: Automatically migrating potentially disruptive changes
export class NgClassMigration {
  // Always migrates multi-class keys, potentially creating verbose output
}

// Good: Making disruptive changes opt-in
export class NgClassMigration {
  constructor(private options: { migrateMultiClassKeys?: boolean } = {}) {}
  
  migrate() {
    // By default don't migrate multi-class keys
    if (!this.options.migrateMultiClassKeys) {
      return; // Skip potentially disruptive migration
    }
    // Only migrate when explicitly requested
  }
}
```

This approach protects users from unexpected changes while still providing access to new functionality when they're ready to adopt it.