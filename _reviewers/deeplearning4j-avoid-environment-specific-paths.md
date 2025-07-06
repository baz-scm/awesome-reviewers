---
title: Avoid environment-specific paths
description: Always use environment variables or configuration mechanisms instead
  of hardcoding paths to compilers, tools, or directories. Hardcoded paths create
  dependencies on specific environments and break compatibility across different platforms
  and CI systems.
repository: deeplearning4j/deeplearning4j
label: Configurations
language: Shell
comments_count: 3
repository_stars: 14036
---

Always use environment variables or configuration mechanisms instead of hardcoding paths to compilers, tools, or directories. Hardcoded paths create dependencies on specific environments and break compatibility across different platforms and CI systems.

Bad:
```bash
#!/bin/bash
CXX=/usr/bin/g++
```

Good:
```bash
#!/bin/bash
# Use environment variable if set, otherwise use default
CXX=${CXX:-g++}
```

For specialized environment paths, use specific environment variables that users can customize:

Bad:
```bash
export CMAKE_COMMAND="$CMAKE_COMMAND -D CMAKE_TOOLCHAIN_FILE=$HOME/raspberrypi/pi.cmake"
```

Good:
```bash
# Allow users to specify RPI_HOME environment variable
export RPI_HOME=${RPI_HOME:-$HOME/raspberrypi}
export CMAKE_COMMAND="$CMAKE_COMMAND -D CMAKE_TOOLCHAIN_FILE=$RPI_HOME/pi.cmake"
```

This approach ensures scripts remain portable across different development environments, CI systems, and operating systems.