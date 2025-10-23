---
title: enhance testing interfaces
description: Design testing tool interfaces to be both flexible and discoverable.
  Support multiple keyword variations for test-related functionality and provide pass-through
  parameter options to enable advanced debugging scenarios.
repository: servo/servo
label: Testing
language: Python
comments_count: 2
repository_stars: 32962
---

Design testing tool interfaces to be both flexible and discoverable. Support multiple keyword variations for test-related functionality and provide pass-through parameter options to enable advanced debugging scenarios.

When implementing testing commands or parsers, consider:
- Allow flexible parameter passing to underlying test tools for debugging purposes (e.g., `--stress-count` for reproducing flaky tests)
- Support multiple keyword variations to make features easily discoverable (e.g., "cov", "coverage", "test-coverage" for the same functionality)
- Design interfaces that accommodate both common use cases and advanced debugging needs

Example implementation:
```python
# Support multiple keywords for discoverability
elif any(word in s for word in ["cov", "coverage", "test-coverage"]):
    return JobConfig("Coverage", Workflow.COVERAGE)

# Allow pass-through parameters for flexibility
@CommandArgument("params", nargs="...", help="Command-line arguments to be passed through to test runner")
```

This approach improves developer experience by making testing tools more accessible and providing the flexibility needed for complex debugging scenarios.