---
title: Document phased migration paths
description: When replacing an existing system feature with a new implementation,
  provide a clear and well-documented phased migration path. Design your system to
  support both old and new approaches simultaneously during a transition period, allowing
  users to migrate gradually without disruption.
repository: opentofu/opentofu
label: Migrations
language: Markdown
comments_count: 2
repository_stars: 25901
---

When replacing an existing system feature with a new implementation, provide a clear and well-documented phased migration path. Design your system to support both old and new approaches simultaneously during a transition period, allowing users to migrate gradually without disruption.

For example, when implementing the S3 locking feature that replaces DynamoDB:

```terraform
# Migration path documentation for users:
# Step 1: Enable both locking mechanisms
terraform {
  backend "s3" {
    bucket = "state-backend"
    key = "statefile"
    region = "us-east-1"
    dynamodb_table = "locking_table" # Old mechanism still present
    use_lockfile = true # New mechanism enabled
  }
}
# Step 2: After successful testing, remove old mechanism
terraform {
  backend "s3" {
    bucket = "state-backend"
    key = "statefile"
    region = "us-east-1"
    use_lockfile = true
  }
}
```

Implementation should handle the transition scenario with special care, such as migrating necessary data between systems, maintaining data integrity, and providing fallback mechanisms. Always include explicit instructions for the recommended migration workflow, including required commands (e.g., `init -reconfigure`) and any behavior changes users should expect during and after migration.