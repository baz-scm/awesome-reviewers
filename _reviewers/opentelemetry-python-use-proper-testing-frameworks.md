---
title: Use proper testing frameworks
description: Always leverage established testing frameworks and APIs over custom bash
  scripts or direct Python execution for test automation. Using proper testing frameworks
  improves maintainability, provides better error handling, and enables more flexible
  test configuration.
repository: open-telemetry/opentelemetry-python
label: Testing
language: Shell
comments_count: 2
repository_stars: 2061
---

Always leverage established testing frameworks and APIs over custom bash scripts or direct Python execution for test automation. Using proper testing frameworks improves maintainability, provides better error handling, and enables more flexible test configuration.

For Python tests:
- Use pytest with appropriate command line options instead of direct script execution
- Configure test environments in tox.ini or pytest.ini files
- Use framework-specific exclusion patterns for skipping tests

Example - Before:
```bash
python test.py http://127.0.0.1:5000/verify-tracecontext
```

Example - After:
```bash
export SERVICE_ENDPOINT=http://127.0.0.1:5000/verify-tracecontext
pytest test.py -k "not test_tracestate_duplicated_keys"
```

For test tooling scripts, prefer language-specific APIs over shell scripts for complex logic. This allows for better error handling and easier maintenance:

```python
# Using a Python API for testing tools instead of bash
from griffe import check

def run_checks(branch="main"):
    # More maintainable than equivalent bash
    results = check.verify_against_branch(branch)
    # Process results with proper error handling
```

Remember to document any test exclusions with clear explanations and FIXMEs for future follow-up.