---
title: Environment variable handling
description: When working with environment variables, follow consistent naming conventions,
  properly check for their presence, and preserve the environment when spawning subprocesses.
  Use standard naming patterns (e.g., `OPENSSL_VERSION_OVERRIDE` instead of `OPEN_SSL_VERSION_OVERRIDE`),
  check both command-line arguments and environment variables for configuration...
repository: duckdb/duckdb
label: Configurations
language: Python
comments_count: 3
repository_stars: 32061
---

When working with environment variables, follow consistent naming conventions, properly check for their presence, and preserve the environment when spawning subprocesses. Use standard naming patterns (e.g., `OPENSSL_VERSION_OVERRIDE` instead of `OPEN_SSL_VERSION_OVERRIDE`), check both command-line arguments and environment variables for configuration options, and always copy the current environment when passing custom environments to subprocess calls.

Example of proper environment handling:
```python
# Good: Standard naming convention
openssl_version = os.getenv("OPENSSL_VERSION_OVERRIDE", "3.0.8")

# Good: Check both argument and environment variable
summarize_failures = args.summarize_failures or os.getenv("SUMMARIZE_FAILURES") == "1"

# Good: Preserve current environment when spawning subprocess
env = os.environ.copy()
if list_of_tests or no_exit or tests_per_invocation:
    env['SUMMARIZE_FAILURES'] = '0'
    env['NO_DUPLICATING_HEADERS'] = '1'
res = subprocess.run(test_cmd, stdout=unittest_stdout, stderr=unittest_stderr, timeout=timeout, env=env)
```

This ensures configuration consistency, prevents loss of important environment settings, and maintains predictable behavior across different execution contexts.