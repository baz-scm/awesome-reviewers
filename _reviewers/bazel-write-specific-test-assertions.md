---
title: Write specific test assertions
description: Make test assertions specific and verifiable rather than relying on generic
  metrics or counts. Use explicit checks for expected behaviors and implement proper
  error handling to ensure tests fail fast when something goes wrong.
repository: bazelbuild/bazel
label: Testing
language: Shell
comments_count: 2
repository_stars: 24489
---

Make test assertions specific and verifiable rather than relying on generic metrics or counts. Use explicit checks for expected behaviors and implement proper error handling to ensure tests fail fast when something goes wrong.

Instead of asserting on generic counts like "2 total actions", verify that specific actions were executed by using detailed logging and targeted assertions:

```bash
# Poor: Generic assertion
expect_log "2 total actions"

# Better: Specific assertion  
bazel build --experimental_ui_debug_all_events //pkg:a
expect_log "Executing genrule //pkg:a"
```

Additionally, use proper error handling mechanisms like `set -e` in shell tests to ensure failures are caught immediately:

```bash
#!/bin/sh
set -e  # Fail fast on any error
touch "$TEST_TMPDIR/test_file"  # Will properly fail if directory not writable
```

This approach makes tests more reliable, easier to debug when they fail, and provides clearer feedback about what specifically went wrong during test execution.