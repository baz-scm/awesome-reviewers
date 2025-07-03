---
title: Standardize makefile patterns
description: 'Maintain consistent Makefile patterns across all components to improve
  build reliability and developer experience in CI/CD pipelines.


  Key practices to follow:'
repository: kubeflow/kubeflow
label: CI/CD
language: Other
comments_count: 5
repository_stars: 15064
---

Maintain consistent Makefile patterns across all components to improve build reliability and developer experience in CI/CD pipelines.

Key practices to follow:

1. Use `.PHONY` targets for all rules to prevent conflicts with actual files:
   ```makefile
   .PHONY: build docker-build docker-push image
   ```

2. Standardize version tagging across components:
   ```makefile
   TAG ?= $(shell git describe --tags --always)
   ```

3. Create consistent build rule patterns across components:
   ```makefile
   docker-build:
       docker build -t ${IMG}:${TAG} -f Dockerfile .

   docker-push:
       docker push ${IMG}:${TAG}

   image: docker-build docker-push
   ```

4. Avoid changing directories in build commands when possible; use Docker's build context parameter instead:
   ```makefile
   # Instead of:
   # cd .. && docker build -t ${IMG}:${TAG} -f Dockerfile .

   # Prefer:
   docker build -t ${IMG}:${TAG} -f Dockerfile ..
   ```

5. Remove unused or deprecated build rules to keep Makefiles maintainable.

These standardized patterns make it easier for developers to work across different components, improve CI/CD pipeline reliability, and reduce confusion when building and deploying components.
