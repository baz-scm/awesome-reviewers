---
title: Respect environment overrides
description: Build systems and configuration scripts must respect standard environment
  variables and provide proper override mechanisms. This ensures flexibility for users
  with different build environments, cross-compilation needs, and custom toolchain
  requirements.
repository: tree-sitter/tree-sitter
label: Configurations
language: Other
comments_count: 4
repository_stars: 21799
---

Build systems and configuration scripts must respect standard environment variables and provide proper override mechanisms. This ensures flexibility for users with different build environments, cross-compilation needs, and custom toolchain requirements.

Always use the `?=` operator in Makefiles to set defaults while allowing environment overrides, and use `override +=` to append mandatory flags:

```make
# Allow environment override with sensible defaults
CFLAGS ?= -O3 -Wall -Wextra
CC ?= clang
# Append mandatory flags that cannot be overridden
override CFLAGS += -std=gnu11 -fPIC -Ilib/include
```

For configuration detection, provide compiler flag overrides as escape hatches:

```c
// Allow compile-time override while providing automatic detection
#if !defined(TS_BIG_ENDIAN)
#if (defined(__BYTE_ORDER__) && __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__)
#define TS_BIG_ENDIAN 1
#else  
#define TS_BIG_ENDIAN 0
#endif
#endif
```

Never hardcode or remove the ability to override critical build variables like CC, CFLAGS, CXXFLAGS, or LDFLAGS. Users may need to specify custom compilers, cross-compilation toolchains, or additional flags for their specific build environments. This principle applies to all build systems including Makefiles, CMake, and custom build scripts.