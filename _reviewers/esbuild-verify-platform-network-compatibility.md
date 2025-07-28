---
title: verify platform network compatibility
description: When adding support for new platforms or architectures, thoroughly verify
  that networking functionality works correctly across different runtime environments
  and build configurations. This includes validating Go version requirements, cross-compilation
  toolchain compatibility, and runtime behavior differences.
repository: evanw/esbuild
label: Networking
language: Other
comments_count: 3
repository_stars: 39161
---

When adding support for new platforms or architectures, thoroughly verify that networking functionality works correctly across different runtime environments and build configurations. This includes validating Go version requirements, cross-compilation toolchain compatibility, and runtime behavior differences.

Key verification steps:
1. Confirm minimum Go version requirements for target platforms (e.g., Go 1.19+ for loong64 architecture)
2. Test cross-compilation with proper toolchain setup, especially for mobile platforms requiring C compilers
3. Validate WebAssembly networking compatibility when deploying to browser environments
4. Verify that network protocols and connection handling work consistently across architectures

Example from the discussions:
```makefile
platform-linux-loong64:
	@$(MAKE) --no-print-directory GOOS=linux GOARCH=loong64 NPMDIR=npm/esbuild-linux-loong64 platform-unixlike
```

Before adding this target, verify that Go 1.19+ is available and that any networking libraries used in the application are compatible with the loong64 architecture. Similarly, for Android ARM builds, ensure the Android SDK C compiler is properly configured for any networking code that requires CGO.