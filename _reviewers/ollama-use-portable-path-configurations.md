---
title: Use portable path configurations
description: 'Build and configuration scripts should use portable path handling techniques
  to ensure they work correctly across different environments and installations. '
repository: ollama/ollama
label: Configurations
language: Shell
comments_count: 3
repository_stars: 145705
---

Build and configuration scripts should use portable path handling techniques to ensure they work correctly across different environments and installations. 

Key practices:
1. **Use wildcards when copying library files** to include all version suffixes:
   ```bash
   # Correct - captures all version suffixes
   cp ${VULKAN_ROOT}/libvulkan.so* "${BUILD_DIR}/bin/"
   
   # Incorrect - only copies the base library file
   cp "${VULKAN_ROOT}/libvulkan.so" "${BUILD_DIR}/bin/"
   ```

2. **Avoid hardcoded absolute paths** in configuration variables. When default paths are needed, make them overridable:
   ```bash
   # Better approach - allows overriding with environment variables
   if [ -z "${VULKAN_ROOT}" ]; then
       # Default only used if not explicitly set
       VULKAN_ROOT=/usr/lib/
   fi
   ```

3. **Use relative paths with `$ORIGIN` for runtime library paths** instead of absolute paths that assume specific installation locations:
   ```bash
   # Better - uses relative paths from binary location
   EXTRA_LIBS="-Wl,-rpath,'$ORIGIN'"
   
   # Avoid - assumes specific installation location
   EXTRA_LIBS="-Wl,-rpath,/opt/intel/oneapi/compiler/latest/lib"
   ```

4. **Be careful with string formatting** in configuration variables to prevent command execution errors:
   ```bash
   # Correct - no space after equals
   DNF_COMPATIBILITY_FMT="addrepo --from-repofile="
   
   # Incorrect - space will cause command parsing issues
   DNF_COMPATIBILITY_FMT="addrepo --from-repofile= "
   ```

Following these practices ensures build scripts and configurations work reliably across different environments, making software more portable and easier to install for end users.