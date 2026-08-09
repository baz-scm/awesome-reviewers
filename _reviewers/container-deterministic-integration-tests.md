---
title: Deterministic Integration Tests
description: 'When modifying integration-test execution or environment setup, prioritize
  determinism and behavioral equivalence.


  1) Don’t assume test-runner flags are interchangeable'
repository: apple/container
label: Testing
language: Other
comments_count: 2
repository_stars: 48787
---

When modifying integration-test execution or environment setup, prioritize determinism and behavioral equivalence.

1) Don’t assume test-runner flags are interchangeable
- If a flag is known to be “experimental” but was added for harness-specific behavior, treat it as part of the stability contract.
- If you replace it (e.g., to avoid toolchain deprecations), require proof that the new flag reproduces the same behavior; otherwise keep the original behavior behind a switch.

2) Make environment cleanliness an explicit, configurable default
- Default to the cleanest setup that yields repeatable results (including removing cached state like kernels/data that can affect outcomes).
- If you want faster runs by preserving state, require an explicit opt-in environment variable (e.g., `PRESERVE_KERNELS=true`) and document it in the Makefile.

Example pattern (Makefile-style):
```make
# Deterministic defaults
PRESERVE_KERNELS ?= false
PARALLEL_WIDTH ?= 2

define CLEAN_APP_DATA
  @echo "Clearing application data under $(APP_ROOT) ..." ; \
  mkdir -p $(APP_ROOT) ; \
  if [ "$(PRESERVE_KERNELS)" = "true" ]; then \
    find "$(APP_ROOT)" -mindepth 1 -maxdepth 1 ! -name kernels -exec rm -rf {} + ; \
  else \
    find "$(APP_ROOT)" -mindepth 1 -maxdepth 1 -exec rm -rf {} + ; \
  fi
endef

# Prefer keeping the known-stable harness behavior unless proven equivalent
# (gate by toolchain/version or expose a switch)
SWIFT_PARALLEL_ARGS ?= --experimental-maximum-parallelization-width $(PARALLEL_WIDTH)

define RUN_CONCURRENT_PASS
  $(SWIFT) test $(INTEGRATION_SWIFT_EXTRA) -c $(BUILD_CONFIGURATION) $(SWIFT_CONFIGURATION) \
    $(SWIFT_PARALLEL_ARGS) \
    --filter "$(CONCURRENT_FILTER)"
endef
```

Apply this standard to any changes in Testing infrastructure code (Makefile scripts, test harnesses, parallelism config, setup/teardown logic) to prevent flaky integration results and toolchain-dependent breakage.