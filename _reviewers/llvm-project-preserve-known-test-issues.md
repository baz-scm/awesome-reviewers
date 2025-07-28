---
title: preserve known test issues
description: When tests exhibit known false positives or false negatives, preserve
  these test cases with clear documentation rather than removing them. This practice
  prevents accidental "fixes" that mask underlying problems and helps track when issues
  are genuinely resolved.
repository: llvm/llvm-project
label: Testing
language: C
comments_count: 2
repository_stars: 33702
---

When tests exhibit known false positives or false negatives, preserve these test cases with clear documentation rather than removing them. This practice prevents accidental "fixes" that mask underlying problems and helps track when issues are genuinely resolved.

As noted in code review discussions, removing tests for known issues can lead to situations where "someone could make a refactor/speedup patch of the check and accidentally fix FP. Without this test, developer wouldn't know he fixed a FP with an NFC patch."

When modifying test expectations:
1. Document why the change occurred (e.g., "existing false negative: #65888 disabled this check")
2. Distinguish between intentional fixes and environmental changes
3. Keep failing tests commented with FIXME or similar markers explaining the known issue

Example approach:
```c
// FIXME: This triggers a false positive: the "passed to same function" heuristic
// can't map the parameter index 1 to A and B because myprint() has no
// parameters.
//     warning: 2 adjacent parameters of 'passedToSameKNRFunction' of similar type ('int')
#if 0
int myprint();
// Test case preserved to track when this FP is actually fixed
#endif
```

This ensures test suite integrity and prevents regression in issue tracking.