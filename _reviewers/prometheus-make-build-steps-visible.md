---
title: Make build steps visible
description: Build processes should provide clear, visible feedback about the operations
  being performed rather than suppressing output or running silently. This transparency
  helps developers understand what's happening during builds, aids in debugging when
  issues occur, and builds confidence that expected operations (like code signing)
  are actually executing.
repository: prometheus/prometheus
label: CI/CD
language: Other
comments_count: 2
repository_stars: 59616
---

Build processes should provide clear, visible feedback about the operations being performed rather than suppressing output or running silently. This transparency helps developers understand what's happening during builds, aids in debugging when issues occur, and builds confidence that expected operations (like code signing) are actually executing.

Avoid suppressing command echoing unnecessarily and add informative echo statements for significant operations that might otherwise be invisible to users.

Example:
```makefile
# Good - visible commands and informative messages
common-build: promu
	@echo ">> building binaries"
	$(PROMU) build --prefix $(PREFIX) $(PROMU_BINARIES)
	@if [ "$(GOHOSTOS)" = "darwin" ] && command -v codesign > /dev/null 2>&1; then \
		echo ">> signing binaries for macOS"; \
		codesign --sign - --force --preserve-metadata=entitlements,requirements,flags,runtime $(PREFIX); \
	fi

# Avoid - suppressed output leaves users uncertain
	@$(PROMU) build --prefix $(PREFIX) $(PROMU_BINARIES) && \
		codesign --sign - --force $(PREFIX) >/dev/null 2>&1
```

This practice is especially important in CI/CD environments where build logs are the primary way to understand and debug automated processes.