---
title: separate build from runtime
description: Dependencies and build requirements should be installed during Docker
  image creation or environment setup, not in runtime execution scripts. This separation
  improves pipeline reliability, reduces execution time, and maintains clear boundaries
  between build and deployment phases.
repository: snyk/cli
label: CI/CD
language: Shell
comments_count: 2
repository_stars: 5178
---

Dependencies and build requirements should be installed during Docker image creation or environment setup, not in runtime execution scripts. This separation improves pipeline reliability, reduces execution time, and maintains clear boundaries between build and deployment phases.

Build-time operations (during Docker image creation):
- Install system dependencies (cmake, libssl-dev, etc.)
- Set up build tools and environments
- Prepare static assets

Runtime operations (during script execution):
- Execute core functionality
- Perform signing, validation, or deployment tasks
- Use pre-installed dependencies

Example of what to avoid:
```bash
# In a signing script - BAD
sudo apt-get update && sudo apt-get install -y cmake libssl-dev libcurl4-openssl-dev faketime
# ... then do signing
```

Instead, install dependencies when building the Docker image, and keep runtime scripts focused on their primary purpose. This also helps avoid issues like Docker buildx tagging problems that can occur when operations are unnecessarily separated across multiple commands.