---
title: Descriptive migration functions
description: Name migration-related functions descriptively to convey their exact
  purpose and context of use. Include detailed documentation explaining when and how
  each function should be executed in the migration workflow. For example, instead
  of ambiguous names like `maintenancerelease`, use more specific terms like `setupBackportBranch`
  or `prepareMaintenanceBranch`...
repository: hashicorp/terraform
label: Migrations
language: Shell
comments_count: 2
repository_stars: 45532
---

Name migration-related functions descriptively to convey their exact purpose and context of use. Include detailed documentation explaining when and how each function should be executed in the migration workflow. For example, instead of ambiguous names like `maintenancerelease`, use more specific terms like `setupBackportBranch` or `prepareMaintenanceBranch` that clearly indicate the function's purpose.

```bash
# BETTER:
# This function sets up a new maintenance branch for accepting backports
# Run this immediately after creating a branch for the previous minor version
function setupBackportBranch {
    # Function implementation
    # ...
}

# AVOID:
# function maintenancerelease {
#     # Unclear purpose without reading implementation
#     # ...
# }
```

Always include brief comments that explain why certain cleanup or setup steps are necessary, making it easier for others to understand and maintain the migration process.