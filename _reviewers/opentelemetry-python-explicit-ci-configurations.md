---
title: Explicit CI configurations
description: 'Always use explicit, specific configurations in CI/CD pipelines to prevent
  ambiguity and conflicts. This includes:


  1. **Clear environment naming** - Use specific environment names to avoid test execution
  conflicts between components. For example, prefer `py3{8,9,10,11,12}-test-opentelemetry-proto-protobuf5`
  over more ambiguous patterns like...'
repository: open-telemetry/opentelemetry-python
label: CI/CD
language: Other
comments_count: 3
repository_stars: 2061
---

Always use explicit, specific configurations in CI/CD pipelines to prevent ambiguity and conflicts. This includes:

1. **Clear environment naming** - Use specific environment names to avoid test execution conflicts between components. For example, prefer `py3{8,9,10,11,12}-test-opentelemetry-proto-protobuf5` over more ambiguous patterns like `py3{8,9,10,11,12}-test-opentelemetry-proto-{0,1}`.

2. **Full paths for output files** - Always specify complete paths for output artifacts to ensure they're generated in the expected location:
```
# Recommended
pytest {toxinidir}/opentelemetry-sdk/benchmarks --benchmark-json={toxinidir}/opentelemetry-sdk/sdk-benchmark.json {posargs}

# Avoid
pytest {toxinidir}/opentelemetry-sdk/benchmarks {posargs} --benchmark-json=sdk-benchmark.json
```

3. **Explicit dependency references** - When dependencies must be pinned to specific versions or commits, clearly document why with comments and references to pending PRs:
```
# Original configuration (will be restored when PR #2687 is merged)
# CONTRIB_REPO_SHA={env:CONTRIB_REPO_SHA:main}
CONTRIB_REPO_SHA=e36889568d1c57c5f6e1dfa65a73519a8eb6607d
```

These practices improve pipeline reliability, reduce debugging time, and make CI configurations more maintainable across the team.