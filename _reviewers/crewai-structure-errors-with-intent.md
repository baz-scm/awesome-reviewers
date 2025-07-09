---
title: Structure errors with intent
description: 'Implement error handling with clear intent and proper propagation. Follow
  these principles:


  1. Use structured try/catch blocks with specific error types'
repository: crewaiinc/crewai
label: Error Handling
language: Python
comments_count: 6
repository_stars: 33945
---

Implement error handling with clear intent and proper propagation. Follow these principles:

1. Use structured try/catch blocks with specific error types
2. Propagate errors explicitly - avoid silent failures
3. Include actionable error messages
4. Consider creating custom exceptions for domain-specific errors

Example of proper error handling structure:

```python
try:
    if self.max_execution_time is not None:
        if not isinstance(self.max_execution_time, int) or self.max_execution_time <= 0:
            raise ValueError("Max Execution time must be a positive integer greater than zero")
        result = self._execute_with_timeout(task_prompt, task, self.max_execution_time)
    else:
        result = self._execute_without_timeout(task_prompt, task)
except TimeoutError as e:
    error = f"Task '{task.description}' execution timed out after {self.max_execution_time} seconds. Consider increasing max_execution_time or optimizing the task."
    crewai_event_bus.emit(
        self,
        event=AgentExecutionErrorEvent(
            agent=self,
            task=task,
            error=error
        )
    )
    raise TimeoutError(error)
```

This pattern ensures:
- Specific error types are caught and handled appropriately
- Error messages are clear and actionable
- Errors are properly propagated up the call stack
- Error state is consistently communicated through events/logging