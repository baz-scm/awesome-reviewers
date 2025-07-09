---
title: Database configuration best practices
description: 'When implementing or modifying database-related configurations, follow
  these principles:


  1. Use semantically appropriate types for configuration parameters (e.g., `Duration`
  instead of `float` for time values)'
repository: vitessio/vitess
label: Database
language: Markdown
comments_count: 2
repository_stars: 19815
---

When implementing or modifying database-related configurations, follow these principles:

1. Use semantically appropriate types for configuration parameters (e.g., `Duration` instead of `float` for time values)
2. Streamline configuration by consolidating related settings (e.g., control transaction behavior through modes rather than multiple flags)
3. Include comprehensive documentation with links to related PRs or issues when documenting database feature changes

**Example:**
```go
// Preferred approach
config.RegisterFlag(Duration("twopc_abandonage", 
                             time.Hour, 
                             "time to wait before abandoning transactions"))

// Instead of
config.RegisterFlag(Float("twopc_abandonage", 
                          3600.0, 
                          "seconds to wait before abandoning transactions"))
config.RegisterFlag(Bool("twopc_enable", 
                         false, 
                         "enable two-phase commit"))
```

For documentation:
```markdown
### Added support for LAST_INSERT_ID(expr)

Added support for `LAST_INSERT_ID(expr)` to align with MySQL behavior, enabling session-level assignment of the last insert ID via query expressions. For more information about this change see [#17295](https://github.com/vitessio/vitess/pull/17295).
```

This approach ensures settings are intuitive to configure, prevents redundancy, and provides clear paths to additional context about database functionality.