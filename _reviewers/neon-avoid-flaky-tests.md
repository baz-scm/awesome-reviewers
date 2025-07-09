---
title: Avoid flaky tests
description: "Tests should be designed to be deterministic and reliable to prevent\
  \ wasted developer time and false confidence. \n\nTwo common causes of flakiness\
  \ to avoid:"
repository: neondatabase/neon
label: Testing
language: Python
comments_count: 3
repository_stars: 19015
---

Tests should be designed to be deterministic and reliable to prevent wasted developer time and false confidence. 

Two common causes of flakiness to avoid:

1. **Time-based waits**: Never rely on `sleep()` calls for synchronization. Instead, use condition-based waits:
```python
# Bad practice
sleep(offload_secs + 1)  # May fail if processing takes longer

# Good practice
wait_until(lambda: check_if_lfc_content_appears_in_remote_storage(), 
           timeout_seconds=10,
           message="LFC content did not appear in remote storage")
```

2. **Shared testing resources**: Use isolated resources for tests instead of shared ones:
```python
# Potentially flaky - using default database
def test_something(neon_simple_env: NeonEnv):
    conn = endpoint.connect()  # Connects to default 'postgres' database
    
# More reliable - using dedicated test database
def test_something(neon_simple_env: NeonEnv):
    conn = endpoint.connect(dbname=f"test_db_{uuid.uuid4()}")
```

Also, follow proper pytest patterns like using `@pytest.mark.skipif` decorators instead of early returns to clearly indicate test conditions and improve maintainability.