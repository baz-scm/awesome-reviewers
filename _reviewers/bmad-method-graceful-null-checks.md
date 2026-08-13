---
title: Graceful Null Checks
description: 'Always treat null/empty/missing required values as first-class cases:
  validate early, and either stop with a clear “HALT-and-ask” (for inputs needed to
  proceed) or conditionally render safe output (to avoid blank placeholders).'
repository: bmad-code-org/bmad-method
label: Null Handling
language: Markdown
comments_count: 2
repository_stars: 51859
---

Always treat null/empty/missing required values as first-class cases: validate early, and either stop with a clear “HALT-and-ask” (for inputs needed to proceed) or conditionally render safe output (to avoid blank placeholders).

How to apply:
- For required inputs (paths, IDs, files):
  - Check non-empty, then existence/format.
  - If invalid, halt further steps and request the missing value from a human (or caller), rather than crashing.
- For templated/structured outputs:
  - Only emit sections that depend on multiple required fields when all are present.
  - Otherwise, fall back to an explicit non-specified/default value to prevent blank placeholders.

Example (combining both patterns):
```pseudo
# Input validation (graceful halt)
if spec_file is empty OR NOT file_exists(spec_file):
  HALT("Provide spec_file path before proceeding")

# Conditional rendering (safe null handling)
if status_file_found == true AND status_update_success == true:
  render("Status Updated + Next Steps using next_workflow/next_agent")
else:
  render("Status not updated; Next Steps: not specified")
```