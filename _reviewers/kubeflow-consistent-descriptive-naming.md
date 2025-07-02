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


[
  {
    "discussion_id": "1216666765",
    "pr_number": 6876,
    "pr_file": "components/pvc-viewer/config/default/kustomization.yaml",
    "created_at": "2023-06-04T12:51:45+00:00",
    "commented_code": "# Adds namespace to all resources.\n# Note: the namespace name needs to be changed here and cannot be changed in an overlay\n# This is because certmanager and webhook use kustomize names to configure resources.\n# Setting another namespace here as in the overlay will lead to e.g. wrong DNSNames being generated.\nnamespace: kubeflow\n\n# Value of this field is prepended to the\n# names of all resources, e.g. a deployment named\n# \"wordpress\" becomes \"alices-wordpress\".\n# Note that it should also match with the prefix (text before '-') of the namespace\n# field above.\nnamePrefix: pvc-viewer-",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1216666765",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6876,
        "pr_file": "components/pvc-viewer/config/default/kustomization.yaml",
        "discussion_id": "1216666765",
        "commented_code": "@@ -0,0 +1,135 @@\n+# Adds namespace to all resources.\n+# Note: the namespace name needs to be changed here and cannot be changed in an overlay\n+# This is because certmanager and webhook use kustomize names to configure resources.\n+# Setting another namespace here as in the overlay will lead to e.g. wrong DNSNames being generated.\n+namespace: kubeflow\n+\n+# Value of this field is prepended to the\n+# names of all resources, e.g. a deployment named\n+# \"wordpress\" becomes \"alices-wordpress\".\n+# Note that it should also match with the prefix (text before '-') of the namespace\n+# field above.\n+namePrefix: pvc-viewer-",
        "comment_created_at": "2023-06-04T12:51:45+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "nit: can we make this `pvcviewer-` instead? In the labels as well we do `pvcviewers` so let's be uniform",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1039531607",
    "pr_number": 6786,
    "pr_file": ".github/workflows/centraldb_angular_frontend_check.yaml",
    "created_at": "2022-12-05T12:30:57+00:00",
    "commented_code": "name: CentralDashboard-angular Frontend check",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1039531607",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6786,
        "pr_file": ".github/workflows/centraldb_angular_frontend_check.yaml",
        "discussion_id": "1039531607",
        "commented_code": "@@ -0,0 +1,34 @@\n+name: CentralDashboard-angular Frontend check",
        "comment_created_at": "2022-12-05T12:30:57+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Let's rename this to `CentralDashboard-angular Frontend Tests` and also the file to `centraldb_angular_frontend_test.yaml`",
        "pr_file_module": null
      }
    ]
  }
]
