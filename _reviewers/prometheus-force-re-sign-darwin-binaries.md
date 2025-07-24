---
title: Force re-sign Darwin binaries
description: When building binaries for macOS (Darwin), always force re-sign them
  to prevent compatibility issues caused by pre-existing signatures. Use the `--force`
  flag with codesign to overwrite any existing signatures that might interfere with
  binary execution.
repository: prometheus/prometheus
label: Security
language: Other
comments_count: 1
repository_stars: 59616
---

When building binaries for macOS (Darwin), always force re-sign them to prevent compatibility issues caused by pre-existing signatures. Use the `--force` flag with codesign to overwrite any existing signatures that might interfere with binary execution.

Code signing is a critical security mechanism that ensures binary integrity and authenticity. However, pre-existing signatures from previous builds or different environments can cause runtime compatibility issues on macOS systems. By force re-signing binaries, you ensure a clean, consistent signature that won't conflict with the target execution environment.

Example implementation:
```makefile
common-build: promu
	@echo ">> building binaries"
	@$(PROMU) build --prefix $(PREFIX) $(PROMU_BINARIES) && \
		if [ "$(GOHOSTOS)" = "darwin" ] && command -v codesign > /dev/null 2>&1; then \
			codesign --sign - --force --preserve-metadata=entitlements,requirements,flags,runtime $(PREFIX) >/dev/null 2>&1; \
		fi
```

This practice ensures that macOS binaries have consistent, valid signatures while maintaining security properties through proper code signing.