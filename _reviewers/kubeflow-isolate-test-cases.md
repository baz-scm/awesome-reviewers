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
