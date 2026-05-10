---
title: Explicit Build Flags
description: Ensure build configuration explicitly sets (1) include paths and (2)
  required language/toolchain modes to prevent environment-dependent header resolution
  and compiler-mode breakages.
repository: redis/redis
label: Configurations
language: Other
comments_count: 2
repository_stars: 74261
---

Ensure build configuration explicitly sets (1) include paths and (2) required language/toolchain modes to prevent environment-dependent header resolution and compiler-mode breakages.

- Include paths: Add third-party include directories explicitly and in a way that selects the intended headers. If a dependency’s headers conflict by name, adjust `-I` order/paths to avoid accidental inclusion of the wrong header.
  
  Example:
  ```make
  # Prefer the dependency’s local includes to avoid header-name collisions
  CFLAGS += -I../deps/tre/local_includes
  ```

- Language standard/toolchain mode: Do not rely on compiler defaults. Set the language standard required by the code (especially for C/C++ standard library features and syntax supported only in newer modes). If the code uses C99-only syntax (e.g., loop variable declarations), configure `-std=c99` so older toolchains can compile successfully.

  Example:
  ```make
  # Required because the code uses C99 syntax (e.g., for (size_t i = ...))
  STD ?= -std=c99
  CFLAGS += $(STD)
  ```

Apply this rule whenever you change a Makefile/feature flag/build script that depends on external headers or compiler behavior—treat build flags and include paths as configuration that must be deterministic across environments.