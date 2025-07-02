---
title: Isolate test cases
description: Create separate test functions for distinct functionality to improve
  test clarity and make failure points more obvious. When writing tests, avoid combining
  multiple scenarios into a single test function.
repository: kubeflow/kubeflow
label: Testing
language: Python
comments_count: 2
repository_stars: 15064
---

Create separate test functions for distinct functionality to improve test clarity and make failure points more obvious. When writing tests, avoid combining multiple scenarios into a single test function.

Instead of adding platform-specific tests to an existing function:

```python
def test_kf_is_ready(namespace, use_basic_auth, use_istio, app_path):
    # General Kubeflow tests
    util.wait_for_deployment(api_client, namespace, deployment_name)
    
    # Platform-specific tests (problematic)
    if platform == "gcp":
        # GCP-specific tests...
```

Create separate test functions:

```python
def test_kf_is_ready(namespace, use_basic_auth, use_istio, app_path):
    # General Kubeflow tests only
    util.wait_for_deployment(api_client, namespace, deployment_name)
    
def test_workload_identity():
    # Skip if not on GCP
    if platform != "gcp":
        pytest.skip("Workload identity test only runs on GCP")
    # GCP-specific tests...
```

This organization makes it immediately clear which specific feature is failing when tests don't pass, simplifies debugging, and enables more effective test filtering when running targeted test suites.


[
  {
    "discussion_id": "336700782",
    "pr_number": 4350,
    "pr_file": "testing/kfctl/kf_is_ready_test.py",
    "created_at": "2019-10-18T22:51:34+00:00",
    "commented_code": "logging.info(\"Verifying that deployment %s started...\", deployment_name)\n    util.wait_for_deployment(api_client, knative_namespace, deployment_name, 10)\n\n  if platform == \"gcp\":",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "336700782",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4350,
        "pr_file": "testing/kfctl/kf_is_ready_test.py",
        "discussion_id": "336700782",
        "commented_code": "@@ -145,6 +145,34 @@ def test_kf_is_ready(namespace, use_basic_auth, use_istio, app_path):\n     logging.info(\"Verifying that deployment %s started...\", deployment_name)\n     util.wait_for_deployment(api_client, knative_namespace, deployment_name, 10)\n \n+  if platform == \"gcp\":",
        "comment_created_at": "2019-10-18T22:51:34+00:00",
        "comment_author": "jlewi",
        "comment_body": "This should be a new test function in this module (a pytest module can have multiple test functions)\r\n\r\ne.g.\r\n\r\n```\r\ntest_workload_identity\r\n```\r\n\r\nWe want separate functions to make it easier to distinguish failures with workload identity versus other tests.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "336700925",
    "pr_number": 4350,
    "pr_file": "testing/kfctl/kf_is_ready_test.py",
    "created_at": "2019-10-18T22:52:22+00:00",
    "commented_code": "logging.info(\"Verifying that deployment %s started...\", deployment_name)\n    util.wait_for_deployment(api_client, knative_namespace, deployment_name, 10)\n\n  if platform == \"gcp\":",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "336700925",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4350,
        "pr_file": "testing/kfctl/kf_is_ready_test.py",
        "discussion_id": "336700925",
        "commented_code": "@@ -145,6 +145,34 @@ def test_kf_is_ready(namespace, use_basic_auth, use_istio, app_path):\n     logging.info(\"Verifying that deployment %s started...\", deployment_name)\n     util.wait_for_deployment(api_client, knative_namespace, deployment_name, 10)\n \n+  if platform == \"gcp\":",
        "comment_created_at": "2019-10-18T22:52:22+00:00",
        "comment_author": "jlewi",
        "comment_body": "Use pytest.Skip to skip the test if we aren't running on GCP\r\nhttp://doc.pytest.org/en/latest/skipping.html",
        "pr_file_module": null
      }
    ]
  }
]
