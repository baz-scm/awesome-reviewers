---
title: Database migration isolation
description: When performing database migrations or schema changes, use containerized
  environments to ensure isolation and comprehensive testing. This approach prevents
  migration issues from affecting development environments and allows for reliable
  rollback scenarios.
repository: block/goose
label: Database
language: Markdown
comments_count: 2
repository_stars: 19037
---

When performing database migrations or schema changes, use containerized environments to ensure isolation and comprehensive testing. This approach prevents migration issues from affecting development environments and allows for reliable rollback scenarios.

Containerized database migrations provide several benefits:
- **Isolation**: Changes are contained within the container, preventing conflicts with local development databases
- **Reproducibility**: Migrations run consistently across different environments
- **Testing**: Full test suites can validate migrations without affecting production data
- **Rollback safety**: Easy to revert to previous database states if issues arise

Example approach for migrating from file-based storage to SQLite:

```bash
# Use container-use to create isolated environment
container-use stdio

# Within the container, perform migration steps:
# 1. Set up SQLite database schema
# 2. Migrate data from file-based storage
# 3. Run comprehensive tests
# 4. Validate data integrity
```

This practice is especially important when transitioning between storage mechanisms (like moving from file-based to database storage) where data integrity and application functionality must be thoroughly validated before deployment.