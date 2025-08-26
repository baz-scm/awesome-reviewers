---
title: Assert null before access
description: When asserting conditions on potentially null pointers, always check
  for null first before accessing the pointer's properties or members. This prevents
  segmentation faults and makes null expectations explicit in the code.
repository: tree-sitter/tree-sitter
label: Null Handling
language: C
comments_count: 2
repository_stars: 21799
---

When asserting conditions on potentially null pointers, always check for null first before accessing the pointer's properties or members. This prevents segmentation faults and makes null expectations explicit in the code.

Instead of writing assertions that could crash on null pointers:
```c
assert(root->ref_count > 0);  // Crashes if root is NULL
```

Use a combined assertion that checks null first:
```c
assert(root && root->ref_count > 0);  // Safe and explicit
```

This pattern serves two purposes: it prevents crashes during debugging when assertions are enabled, and it clearly documents that the code expects the pointer to be non-null. When removing null checks, ensure the underlying assumptions about null safety have actually changed and document why the check is no longer needed.