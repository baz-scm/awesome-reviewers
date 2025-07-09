---
title: Test behavior not calls
description: Tests should validate actual system behavior rather than just verifying
  method calls. When writing tests, focus on asserting the expected outcomes and side
  effects rather than simply checking if methods were invoked.
repository: crewaiinc/crewai
label: Testing
language: Python
comments_count: 3
repository_stars: 33945
---

Tests should validate actual system behavior rather than just verifying method calls. When writing tests, focus on asserting the expected outcomes and side effects rather than simply checking if methods were invoked.

Bad example:
```python
def test_task_execution():
    with patch.object(Agent, "_execute", return_value="ok") as execute:
        result = task.execute()
        assert result.raw == "ok"
        execute.assert_called_once()  # Only validates the call
```

Good example:
```python
@tool("test_tool", result_as_answer=True)
def delayed_tool():
    sleep(5)  # Actual behavior
    return "ok"

def test_task_execution():
    agent = Agent(tools=[delayed_tool])
    task = Task(description="test", agent=agent)
    
    result = task.execute()
    assert result.raw == "ok"
    # Test validates actual timing behavior
    assert task.execution_time >= 5
```

Key points:
- Test real functionality instead of implementation details
- Use actual components when possible rather than mocks
- When mocking is necessary, validate the complete interaction flow
- Include assertions for side effects and timing when relevant
- Focus on behavior that matters to end users