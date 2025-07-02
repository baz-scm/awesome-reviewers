---
title: Automate style enforcement
description: 'Configure your development environment to automatically enforce code
  style standards rather than relying on manual checks during code review. This includes:'
repository: kubeflow/kubeflow
label: Code Style
language: Yaml
comments_count: 2
repository_stars: 15064
---

Configure your development environment to automatically enforce code style standards rather than relying on manual checks during code review. This includes:

1. Use modern, actively maintained linting tools instead of deprecated ones (e.g., replace tslint with eslint)
2. Configure your IDE to automatically apply formatting rules, such as adding newlines at end of files

Example IDE configuration for VSCode (settings.json):
```json
{
  "files.insertFinalNewline": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```

This approach reduces style-related comments in code reviews, ensures consistency across the codebase, and allows reviewers to focus on more substantive issues.


[
  {
    "discussion_id": "1039529505",
    "pr_number": 6786,
    "pr_file": ".github/workflows/centraldb_angular_backend_check.yaml",
    "created_at": "2022-12-05T12:28:44+00:00",
    "commented_code": "name: CentralDashboard-angular Backend check\non:\n  pull_request:\n    paths:\n      - components/centraldashboard-angular/backend/**\n\njobs:\n  run-backend-unittests:\n    name: Unit tests\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v3\n      - uses: actions/setup-node@v3\n        with:\n          node-version: 12\n      - name: Run unit tests\n        run: |\n          cd components/centraldashboard-angular/backend/\n          npm i\n          npm run test\n\n  run-backend-tslint:",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1039529505",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6786,
        "pr_file": ".github/workflows/centraldb_angular_backend_check.yaml",
        "discussion_id": "1039529505",
        "commented_code": "@@ -0,0 +1,34 @@\n+name: CentralDashboard-angular Backend check\n+on:\n+  pull_request:\n+    paths:\n+      - components/centraldashboard-angular/backend/**\n+\n+jobs:\n+  run-backend-unittests:\n+    name: Unit tests\n+    runs-on: ubuntu-latest\n+    steps:\n+      - uses: actions/checkout@v3\n+      - uses: actions/setup-node@v3\n+        with:\n+          node-version: 12\n+      - name: Run unit tests\n+        run: |\n+          cd components/centraldashboard-angular/backend/\n+          npm i\n+          npm run test\n+\n+  run-backend-tslint:",
        "comment_created_at": "2022-12-05T12:28:44+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "We should look into moving away from `tslint` in the backend as well, now that we've decoupled the frontend and backend code",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "618186426",
    "pr_number": 5761,
    "pr_file": "components/profile-controller/config/overlays/kubeflow/namespace-labels.yaml",
    "created_at": "2021-04-22T08:21:05+00:00",
    "commented_code": "# Below is a list of labels to be set by default.\n#\n# To add a namespace label, use `key: 'value'`, for example:\n# istio.io/rev: 'asm-191-1'\n#\n# To remove a namespace label, use `key: ''` to remove key, for example:\n# istio-injection: ''\n# \n# Profile controller will not replace value if namespace label already exists.\n# But profile controller keeps removing namespace label if removing is specified here.\n# In order to change this enforcement:\n# 1. If your profile already has this label:\n#       First, remove this label by using `key: ''` and deploy.\n#       Second, add this label by using `key: 'value'` and deploy.\n# 2. If your profile doesn't have this label:\n#       you can add label and value to this file and deploy.\n# Reason:\n#    Profile controller will enforce flag removal, but not enforce value replacement.\n#   \nkatib-metricscollector-injection:      'enabled'\nserving.kubeflow.org/inferenceservice: 'enabled'\npipelines.kubeflow.org/enabled:        'true'\napp.kubernetes.io/part-of:             'kubeflow-profile'",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "618186426",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5761,
        "pr_file": "components/profile-controller/config/overlays/kubeflow/namespace-labels.yaml",
        "discussion_id": "618186426",
        "commented_code": "@@ -0,0 +1,23 @@\n+# Below is a list of labels to be set by default.\n+#\n+# To add a namespace label, use `key: 'value'`, for example:\n+# istio.io/rev: 'asm-191-1'\n+#\n+# To remove a namespace label, use `key: ''` to remove key, for example:\n+# istio-injection: ''\n+# \n+# Profile controller will not replace value if namespace label already exists.\n+# But profile controller keeps removing namespace label if removing is specified here.\n+# In order to change this enforcement:\n+# 1. If your profile already has this label:\n+#       First, remove this label by using `key: ''` and deploy.\n+#       Second, add this label by using `key: 'value'` and deploy.\n+# 2. If your profile doesn't have this label:\n+#       you can add label and value to this file and deploy.\n+# Reason:\n+#    Profile controller will enforce flag removal, but not enforce value replacement.\n+#   \n+katib-metricscollector-injection:      'enabled'\n+serving.kubeflow.org/inferenceservice: 'enabled'\n+pipelines.kubeflow.org/enabled:        'true'\n+app.kubernetes.io/part-of:             'kubeflow-profile'",
        "comment_created_at": "2021-04-22T08:21:05+00:00",
        "comment_author": "Bobgy",
        "comment_body": "nit: generally, always add a newline at end of file. Same for other files\r\n\r\nYou can configure your IDE to automatically do that.",
        "pr_file_module": null
      },
      {
        "comment_id": "618731511",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5761,
        "pr_file": "components/profile-controller/config/overlays/kubeflow/namespace-labels.yaml",
        "discussion_id": "618186426",
        "commented_code": "@@ -0,0 +1,23 @@\n+# Below is a list of labels to be set by default.\n+#\n+# To add a namespace label, use `key: 'value'`, for example:\n+# istio.io/rev: 'asm-191-1'\n+#\n+# To remove a namespace label, use `key: ''` to remove key, for example:\n+# istio-injection: ''\n+# \n+# Profile controller will not replace value if namespace label already exists.\n+# But profile controller keeps removing namespace label if removing is specified here.\n+# In order to change this enforcement:\n+# 1. If your profile already has this label:\n+#       First, remove this label by using `key: ''` and deploy.\n+#       Second, add this label by using `key: 'value'` and deploy.\n+# 2. If your profile doesn't have this label:\n+#       you can add label and value to this file and deploy.\n+# Reason:\n+#    Profile controller will enforce flag removal, but not enforce value replacement.\n+#   \n+katib-metricscollector-injection:      'enabled'\n+serving.kubeflow.org/inferenceservice: 'enabled'\n+pipelines.kubeflow.org/enabled:        'true'\n+app.kubernetes.io/part-of:             'kubeflow-profile'",
        "comment_created_at": "2021-04-22T20:53:58+00:00",
        "comment_author": "zijianjoy",
        "comment_body": "Thank you Yuan! I updated my IDE for keeping newline at the end of file.",
        "pr_file_module": null
      }
    ]
  }
]
