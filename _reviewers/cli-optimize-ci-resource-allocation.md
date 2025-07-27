---
title: optimize CI resource allocation
description: Match CI/CD resource allocation to actual job requirements rather than
  using oversized configurations globally. Create specialized executors and resource
  classes for different job types to optimize cost and performance.
repository: snyk/cli
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 5178
---

Match CI/CD resource allocation to actual job requirements rather than using oversized configurations globally. Create specialized executors and resource classes for different job types to optimize cost and performance.

This practice prevents unnecessary resource waste when jobs with different computational needs share the same executor configuration. Instead of applying large resource classes universally, analyze each job's actual requirements and provision accordingly.

**Implementation approach:**
- Create job-specific executors with appropriate resource classes
- Use smaller resource classes for lightweight jobs (linting, no-ops, simple builds)
- Reserve larger resource classes only for computationally intensive jobs (tests, compilation)
- Leverage caching strategies that account for different tool subsets rather than installing everything everywhere

**Example:**
```yaml
executors:
  docker-amd64:
    docker:
      - image: bastiandoetsch209/cli-build:20240214-145818
    working_directory: /mnt/ramdisk/snyk
    resource_class: large
    
  docker-amd64-xl:  # Only for resource-intensive jobs
    docker:
      - image: bastiandoetsch209/cli-build:20240214-145818
    working_directory: /mnt/ramdisk/snyk
    resource_class: xlarge

  noop:
    docker:
      - image: cimg/base:current
    resource_class: small  # Minimal resources for no-op jobs

jobs:
  acceptance-test:
    executor: docker-amd64-xl  # Use xlarge only where needed
    
  simple-validation:
    executor: noop  # Use small resources for lightweight tasks
```

This approach reduces infrastructure costs while maintaining performance where it matters most, and prevents the common anti-pattern of over-provisioning resources across all pipeline jobs.