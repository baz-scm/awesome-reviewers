---
name: isolate-test-environments
description: 'Tests should be isolated from the production environment to prevent
  side effects and ensure reproducibility. This principle has two main applications:'
version: '1.0'
---
# Isolate test environments

Tests should be isolated from the production environment to prevent side effects and ensure reproducibility. This principle has two main applications:

1. **Use proper temporary files**: Instead of writing test files to the current directory where they might overwrite real files, use the `tempfile` module to create isolated test files.

2. **Establish correct directory context**: Ensure tests run in the appropriate directory context to prevent location-dependent failures.

Example:
```python
# Good: Use temporary files instead of hardcoded paths
import tempfile
message_file_path = tempfile.mktemp()
main(["--message-file", message_file_path], input=DummyInput(), output=DummyOutput())

# Good: Explicitly set the directory context for tests
with change_dir(testdir):
    # Test code runs in the correct context
    # ...
```

Following these practices prevents tests from accidentally modifying real files and ensures they'll run consistently regardless of the current working directory.
