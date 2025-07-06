---
title: Cross-platform feature flags
description: When documenting package installation commands with feature flags, ensure
  compatibility across different operating systems. Windows handles quoted package
  specifications differently than Unix-based systems, which can lead to installation
  failures.
repository: pola-rs/polars
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 34296
---

When documenting package installation commands with feature flags, ensure compatibility across different operating systems. Windows handles quoted package specifications differently than Unix-based systems, which can lead to installation failures.

For maximum compatibility in documentation, use double quotes or provide OS-specific instructions:

```bash
# Most compatible approach across platforms
pip install "polars[feature]"

# Or provide platform-specific examples when needed
# For Unix/MacOS:
pip install 'polars[feature]'

# For Windows:
pip install polars[feature]
```

This approach ensures users can successfully install packages with feature flags regardless of their operating system, reducing confusion and installation errors. When providing environment-specific configuration instructions (like for CUDA 11 systems), clearly indicate which environments require additional steps and separate them from general instructions.