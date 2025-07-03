---
title: Centralize configuration parameters
description: 'Avoid hardcoded paths and duplicated configuration values throughout
  the code. Instead:


  1. Use dedicated configuration files for settings that appear in multiple places'
repository: apache/mxnet
label: Configurations
language: Shell
comments_count: 3
repository_stars: 20801
---

Avoid hardcoded paths and duplicated configuration values throughout the code. Instead:

1. Use dedicated configuration files for settings that appear in multiple places
2. Leverage environment variables for runtime path configurations
3. Implement runtime detection for system-specific paths when possible
4. When environment setup scripts are available (like `source /opt/intel/oneapi/setvars.sh`), prefer them over hardcoding paths

Example of problematic code:
```bash
# Hardcoded path that may not work across installations
export CPATH=/opt/arm/armpl_21.0_gcc-8.2/include_lp64_mp:$CPATH
# Duplicated test configuration
pytest -m 'not serial' -k 'not test_operator' -n 4 --durations=50 --cov-report xml:tests_unittest.xml --verbose tests/python/unittest
```

Better approach:
```bash
# Use environment detection or user configuration
if [[ -d "${ARM_PATH}" ]]; then
    export CPATH=${ARM_PATH}/include_lp64_mp:$CPATH
fi

# Load configuration from a central file
source ./test_config.sh
pytest ${TEST_COMMON_ARGS} ${UNITTEST_ARGS} tests/python/unittest
```

This approach improves portability across different environments and makes maintenance easier when configurations need to change.
