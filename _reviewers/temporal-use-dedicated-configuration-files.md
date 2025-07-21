---
title: Use dedicated configuration files
description: Always use dedicated configuration files for specific configuration needs
  rather than modifying core build or system files. This practice improves maintainability,
  traceability, and scope control.
repository: temporalio/temporal
label: Configurations
language: Other
comments_count: 3
repository_stars: 14953
---

Always use dedicated configuration files for specific configuration needs rather than modifying core build or system files. This practice improves maintainability, traceability, and scope control.

When working with configuration:
- Use specialized configuration files (e.g., `buf.yaml` for build ignores) instead of modifying core build files like Makefiles
- Add explanatory comments when configuration approaches might not be obvious
- Implement scoped configurations rather than global changes when possible
- Always pin dependency versions to specific versions rather than using "latest" to ensure predictable behavior

Example:
```
# Don't do this:
# In Makefile
ci-build-misc: \
	clean-tools \
	proto \
	go-generate \
	# buf-breaking was removed here

# Instead do this:
# 1. Keep the Makefile entry
ci-build-misc: \
	clean-tools \
	proto \
	go-generate \
	buf-breaking \  # Don't remove this, add ignores to proto/internal/buf.yaml instead

# 2. Add specific ignores in the dedicated configuration file (buf.yaml)

# 3. For tool dependencies, use specific versions:
WORKFLOWCHECK := $(LOCALBIN)/workflowcheck
$(WORKFLOWCHECK): | $(LOCALBIN)
	$(call go-install-tool,$(WORKFLOWCHECK),go.temporal.io/sdk/contrib/tools/workflowcheck,v0.3.0)
```

This approach keeps configuration changes properly scoped, makes them easier to track, and prevents unintended consequences from global modifications or unexpected version changes.