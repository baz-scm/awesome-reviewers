---
title: Manage test environments
description: 'When writing tests that interact with environment variables or configuration
  settings, always (1) preserve the original state and (2) explicitly specify required
  configurations. '
repository: boto/boto3
label: Configurations
language: Python
comments_count: 3
repository_stars: 9417
---

When writing tests that interact with environment variables or configuration settings, always (1) preserve the original state and (2) explicitly specify required configurations. 

For environment variables, use setUp/tearDown methods to save and restore their state after test execution:

```python
def restore_dict(self, dictionary: dict, original_data: dict):
    dictionary.clear()
    dictionary.update(original_data)

def setUp(self):
    # Save original environment to restore after test
    original_env = os.environ.copy()
    self.addCleanup(lambda: self.restore_dict(os.environ, original_env))
```

For service configurations, always explicitly specify required parameters like region rather than relying on the machine's environment:

```python
self.session = boto3.session.Session(region_name='us-west-2')
```

This practice ensures tests are isolated, repeatable, and portable across different development environments, preventing unexpected test failures and interference between test cases.