---
title: comprehensive test verification
description: Write tests that comprehensively verify functionality by covering related
  scenarios and testing complete outputs rather than partial matches. This approach
  makes tests more resilient to code changes and ensures thorough validation.
repository: denoland/deno
label: Testing
language: Other
comments_count: 2
repository_stars: 103714
---

Write tests that comprehensively verify functionality by covering related scenarios and testing complete outputs rather than partial matches. This approach makes tests more resilient to code changes and ensures thorough validation.

When testing a feature, consider testing related functionality that users might invoke in similar contexts. For example, if testing `deno add --npm`, also test `deno install` and related command variations.

Additionally, prefer testing complete outputs over partial matches using wildcards. Instead of testing only fragments, verify the full output to catch unintended changes:

```jsonc
// Less resilient - partial output testing
"output": "[WILDCARD]Found 1 problem"

// More resilient - complete output testing  
"output": "[WILDCARD]Found 1 problem\nChecked 1 file"
```

This ensures tests catch when fixes or messages are moved, modified, or when output format changes unexpectedly.