---
title: Use semantic identifiers
description: Choose semantically appropriate identifiers and types that clearly represent
  their purpose. This includes using the correct data type (e.g., boolean for flags
  instead of integers) and ensuring proper spelling of all identifiers.
repository: torvalds/linux
label: Naming Conventions
language: C
comments_count: 2
repository_stars: 197350
---

Choose semantically appropriate identifiers and types that clearly represent their purpose. This includes using the correct data type (e.g., boolean for flags instead of integers) and ensuring proper spelling of all identifiers.

For boolean flags:
```c
// Not recommended
int reboot_default = 0;  // Using integer for a boolean flag

// Recommended
bool reboot_default = false;  // Clear semantic meaning
```

For function and variable names:
- Verify spelling correctness (e.g., "local_irq_save" not "ocal_irq_save")
- Choose names that accurately reflect the purpose or behavior

Using semantically appropriate identifiers improves code readability, reduces bugs, and makes maintenance easier by clearly expressing intent.