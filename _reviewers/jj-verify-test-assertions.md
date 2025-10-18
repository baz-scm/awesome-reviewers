---
title: Verify test assertions
description: Always use appropriate assertion methods in tests to ensure proper verification
  of command behavior. When you don't need to examine command output, use `.success()`
  to verify the command completed without errors. When the output content is meaningful
  for testing the functionality, capture and snapshot it for verification.
repository: jj-vcs/jj
label: Testing
language: Rust
comments_count: 2
repository_stars: 21171
---

Always use appropriate assertion methods in tests to ensure proper verification of command behavior. When you don't need to examine command output, use `.success()` to verify the command completed without errors. When the output content is meaningful for testing the functionality, capture and snapshot it for verification.

**Problematic approach:**
```rust
// Ignoring output when we should verify success
let _output = test_env.run_jj_in(&workspace_root, ["git", "colocation", "enable"]);

// Using .success() when output should be verified
work_dir.run_jj(["metaedit", "--author-timestamp", "2001-02-03 04:05:14.000+07:00"]).success();
```

**Better approach:**
```rust
// Use .success() when only caring about command completion
test_env.run_jj_in(&workspace_root, ["git", "colocation", "enable"]).success();

// Snapshot output when it's meaningful for verification
let output = work_dir.run_jj(["metaedit", "--author-timestamp", "2001-02-03 04:05:14.000+07:00"]);
insta::assert_snapshot!(output, @"...");
```

This practice ensures that tests properly verify both command success and expected behavior, making test failures more informative and catching regressions in command output or error handling.