---
title: Purpose-reflecting file names
description: File names should clearly communicate their purpose and functionality.
  Avoid generic, ambiguous, or numbered names (like "Makefile2") that don't convey
  the file's actual role or lead to recurring questions.
repository: ollama/ollama
label: Naming Conventions
language: Other
comments_count: 2
repository_stars: 145705
---

File names should clearly communicate their purpose and functionality. Avoid generic, ambiguous, or numbered names (like "Makefile2") that don't convey the file's actual role or lead to recurring questions.

Choose names that:
1. Reflect the file's specific purpose (e.g., "vendor.make" for vendoring operations)
2. Avoid conflicts with convention-based names that carry specific expectations
3. Prevent confusion with automatically generated files

For example, instead of:
```
Makefile2  # What does the "2" mean? What is this for?
```

Use:
```
vendor.make  # Clearly indicates this handles vendoring operations
```

This practice enhances code maintainability and reduces onboarding time for new developers, who can understand a file's purpose at a glance rather than having to investigate its contents or ask questions.