---
title: Consistent descriptive naming
description: 'Maintain consistency in naming patterns across related resources while
  ensuring names accurately reflect their purpose. When naming components, files,
  or configurations:'
repository: kubeflow/kubeflow
label: Naming Conventions
language: Yaml
comments_count: 2
repository_stars: 15064
---

Maintain consistency in naming patterns across related resources while ensuring names accurately reflect their purpose. When naming components, files, or configurations:

1. Use the same naming pattern for related components (e.g., if using "pvcviewer" in labels, use "pvcviewer-" as prefix rather than "pvc-viewer-")
2. Choose names that precisely reflect the component's purpose (e.g., "test" rather than "check" for testing workflows)
3. Apply naming conventions consistently across configuration files, code, and documentation

Example:
```yaml
# Good
namespace: kubeflow
namePrefix: pvcviewer-  # Consistent with label "pvcviewers" used elsewhere

# Avoid
namespace: kubeflow
namePrefix: pvc-viewer-  # Inconsistent with "pvcviewers" label
```

For workflow files, use names that accurately describe their function:
```yaml
# Good
name: CentralDashboard-angular Frontend Tests
# filename: centraldb_angular_frontend_test.yaml

# Avoid
name: CentralDashboard-angular Frontend check
# filename: centraldb_angular_frontend_check.yaml
```
