---
title: Centralize shared configurations
description: When adding common functionality like help targets, build rules, or other
  configuration elements that will be used across multiple projects or subdirectories,
  prefer centralizing them in shared configuration files rather than duplicating the
  implementation.
repository: prometheus/prometheus
label: Configurations
language: Other
comments_count: 2
repository_stars: 59616
---

When adding common functionality like help targets, build rules, or other configuration elements that will be used across multiple projects or subdirectories, prefer centralizing them in shared configuration files rather than duplicating the implementation.

For Makefiles, use a common include file (like Makefile.common) that can be propagated across the organization. This approach reduces duplication, ensures consistency, and simplifies maintenance when changes are needed.

Example:
Instead of adding the same help target to multiple Makefiles:
```makefile
# In each subdirectory Makefile
help: ## Displays commands and their descriptions.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
```

Centralize it in Makefile.common and include it:
```makefile
# In subdirectory Makefiles
include ../../Makefile.common
```

This pattern applies to other configuration files as well - look for opportunities to extract common configuration elements into shared, includable files that can be maintained centrally and distributed across projects.