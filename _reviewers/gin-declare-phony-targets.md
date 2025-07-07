---
title: Declare .PHONY targets
description: Always explicitly declare all Makefile targets that don't create files
  as `.PHONY`. This prevents conflicts with potential files of the same name, makes
  build intentions clear, and increases reliability in CI/CD pipelines.
repository: gin-gonic/gin
label: CI/CD
language: Other
comments_count: 2
repository_stars: 83022
---

Always explicitly declare all Makefile targets that don't create files as `.PHONY`. This prevents conflicts with potential files of the same name, makes build intentions clear, and increases reliability in CI/CD pipelines.

For better readability and maintenance, place the `.PHONY` declaration directly above the corresponding target:

```makefile
.PHONY: deps
deps:
    go get -d -v github.com/dustin/go-broadcast/...

.PHONY: build
build: deps
    go build -o realtime-chat main.go rooms.go template.go
```

Rather than grouping all `.PHONY` declarations at the end or beginning of the Makefile, this pattern makes the relationship between declarations and targets obvious at a glance, reducing the chance of forgetting to update declarations when adding new targets.