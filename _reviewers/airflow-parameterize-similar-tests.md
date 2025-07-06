---
title: Parameterize similar tests
description: Write parameterized tests instead of using for loops or duplicating test
  code for similar test cases. Using pytest's `@pytest.mark.parametrize` decorator
  improves test maintainability, provides clearer failure messages, and makes the
  test structure more readable.
repository: apache/airflow
label: Testing
language: Python
comments_count: 4
repository_stars: 40858
---

Write parameterized tests instead of using for loops or duplicating test code for similar test cases. Using pytest's `@pytest.mark.parametrize` decorator improves test maintainability, provides clearer failure messages, and makes the test structure more readable.

Instead of:
```python
def test__read_for_executor_fallbacks(self, create_task_instance):
    for state in (TaskInstanceState.RUNNING, TaskInstanceState.DEFERRED, TaskInstanceState.UP_FOR_RETRY):
        ti = create_task_instance(dag_id="test_dag", task_id="test_task")
        ti.state = state
        # Test implementation with same logic for each state
        ...
```

Use:
```python
@pytest.mark.parametrize(
    "state",
    [TaskInstanceState.RUNNING, TaskInstanceState.DEFERRED, TaskInstanceState.UP_FOR_RETRY]
)
def test__read_for_executor_fallbacks(self, state, create_task_instance):
    ti = create_task_instance(dag_id="test_dag", task_id="test_task")
    ti.state = state
    # Test implementation
    ...
```

This approach applies to other types of test parameterization as well, such as organizing related test cases together in parameterized test functions rather than duplicating test logic with slight variations. For endpoint testing, organize tests with one class per endpoint and multiple parameterized test methods for different test cases.