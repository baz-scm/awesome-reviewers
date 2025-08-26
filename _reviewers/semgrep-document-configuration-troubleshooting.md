---
title: Document configuration troubleshooting
description: Configuration files and scripts should include comprehensive documentation
  that helps developers understand their purpose, scope, and how to troubleshoot common
  issues. This includes adding comments that explain what the configuration does,
  what errors might occur, and specific steps to resolve them.
repository: semgrep/semgrep
label: Configurations
language: Shell
comments_count: 3
repository_stars: 12598
---

Configuration files and scripts should include comprehensive documentation that helps developers understand their purpose, scope, and how to troubleshoot common issues. This includes adding comments that explain what the configuration does, what errors might occur, and specific steps to resolve them.

Key elements to include:
- Clear description of the file's purpose and scope
- Troubleshooting instructions for common error scenarios
- Guidance on how to modify the configuration when adding dependencies or features
- References to related configuration files or tools

Example from a build configuration script:
```bash
#!/usr/bin/env bash
# Setup the opam environment under MacOS to build and release semgrep-core.
# All other MacOS-related setup should be in `osx-setup-post-opam-for-release.sh`

# If you added a dependency that's causing a linking error:
# 1. Use `opam depext` to find required system libraries
# 2. Add the library to the appropriate CCLIB array below
# 3. For language dependencies, add to the LANGS array
```

This approach prevents developers from having to reverse-engineer configuration files and reduces time spent debugging environment-specific issues. When errors occur, developers can quickly identify what needs to be modified and how to make the necessary changes.