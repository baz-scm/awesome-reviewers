---
title: Environment variable management
description: 'Manage environment variables in Docker configurations with appropriate
  scope, placement, and documentation:


  1. **Set environment variables with appropriate scope**:'
repository: kubeflow/kubeflow
label: Configurations
language: Dockerfile
comments_count: 5
repository_stars: 15064
---

Manage environment variables in Docker configurations with appropriate scope, placement, and documentation:

1. **Set environment variables with appropriate scope**:
   - Use variables only where needed, not globally
   - Set temporary variables like `DEBIAN_FRONTEND` only within the commands that need them:
   ```dockerfile
   # Do this:
   RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
       package1 package2
   
   # Not this:
   ENV DEBIAN_FRONTEND=noninteractive
   RUN apt-get update && apt-get install -y package1 package2
   ```

2. **Place variables logically**:
   - Group related variables under descriptive comments
   - Place variables near their related commands
   - Use ARG instead of ENV for build-time values, especially versions:
   ```dockerfile
   # version details
   ARG LIBFABRIC_VERSION="1.20.0"
   ARG PYTORCH_VERSION="2.2.2"
   ```

3. **Document variables properly**:
   - Add comments explaining non-obvious configurations
   - Include links to relevant documentation when appropriate
   - Document compatibility requirements:
   ```dockerfile
   # Gaudi does not currently support Python 3.11, so we downgrade to 3.10
   # https://docs.habana.ai/en/latest/Support_Matrix/Support_Matrix.html
   ```

4. **Clean up unnecessary variables**:
   - Remove obsolete or unused environment variables
   - Consider using dedicated configuration files under /etc/ instead of environment variables when appropriate
