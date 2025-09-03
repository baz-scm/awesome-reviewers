---
title: avoid `-count=1` flag
description: Avoid using the `-count=1` flag in Go test commands unless specifically
  required to disable test caching. Removing this flag enables concurrent test execution,
  which not only improves test performance but more importantly allows for better
  detection of data races during testing.
repository: gofiber/fiber
label: Testing
language: Yaml
comments_count: 2
repository_stars: 37560
---

Avoid using the `-count=1` flag in Go test commands unless specifically required to disable test caching. Removing this flag enables concurrent test execution, which not only improves test performance but more importantly allows for better detection of data races during testing.

The `-count=1` flag disables Go's test caching mechanism and forces tests to run sequentially. While this was historically used to work around caching issues, modern Go testing benefits from concurrent execution for race detection.

Example of preferred approach:
```bash
# Preferred - enables concurrency and race detection
go test -v -race ./...

# Avoid unless caching must be disabled
go test -v -race -count=1 ./...
```

When tests run concurrently with the `-race` flag, they are more likely to expose data races and concurrency issues that might be missed in sequential execution. This approach has proven effective in practice, as concurrent test execution can immediately surface race conditions that would otherwise remain hidden.