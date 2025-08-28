---
title: optimize CI resource usage
description: Design CI workflows to maximize resource efficiency by reusing build
  artifacts across jobs whenever possible, while carefully evaluating when separate
  builds are truly necessary. Before creating duplicate build jobs, assess whether
  different compilation flags or configurations genuinely require separate builds,
  or if the same artifacts can be reused with...
repository: cloudflare/workerd
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 6989
---

Design CI workflows to maximize resource efficiency by reusing build artifacts across jobs whenever possible, while carefully evaluating when separate builds are truly necessary. Before creating duplicate build jobs, assess whether different compilation flags or configurations genuinely require separate builds, or if the same artifacts can be reused with additional steps.

Consider these strategies:
- Reuse existing job artifacts for additional testing or analysis steps
- Evaluate whether custom build configurations justify separate jobs
- Use larger runners when build duplication is unavoidable to reduce overall duration
- Take incremental approaches to dependency updates to maintain stability

Example from workflow optimization:
```yaml
# Instead of separate benchmark build job
- name: Build benchmarks  
  run: bazel build ${{ env.BAZEL_ARGS }} //src/workerd/tests:all_benchmarks

# Consider reusing existing build artifacts:
- name: Run benchmarks
  uses: existing-build-artifacts
  run: ./run-benchmarks-on-existing-binary
```

This approach reduces CI costs, improves pipeline efficiency, and minimizes resource waste while ensuring all build requirements are met.