---
title: Keep configurations current
description: Ensure all configuration elements (dependencies, build settings, preprocessor
  flags) are up-to-date, documented, and consistent with project standards. This practice
  prevents issues arising from outdated references and improves maintainability for
  team members.
repository: deeplearning4j/deeplearning4j
label: Configurations
language: Other
comments_count: 4
repository_stars: 14036
---

Ensure all configuration elements (dependencies, build settings, preprocessor flags) are up-to-date, documented, and consistent with project standards. This practice prevents issues arising from outdated references and improves maintainability for team members.

Key practices include:

1. Document special configuration elements in README files or documentation:
```
// In NecAurora.md:
// .vc/.vcpp file extensions are used to differentiate VE device files 
// from c/cpp in cmake. Cmake will compile them using nec.
```

2. Update preprocessor definitions when dependencies change names or versions:
```cpp
-#ifdef HAVE_MKLDNN
+#ifdef HAVE_ONEDNN
// Updated to reflect new dependency name
```

3. Maintain consistent tool versions across related projects (e.g., same Maven version for all modules)

4. Verify third-party dependencies comply with organizational policies before inclusion, especially for licensing requirements

Regularly audit configuration files to ensure they remain aligned with current technologies, dependency versions, and organizational standards.