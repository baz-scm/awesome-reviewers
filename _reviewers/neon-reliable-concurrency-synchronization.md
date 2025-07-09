---
title: Reliable concurrency synchronization
description: When handling concurrent operations, prefer completion signals and proper
  thread management over arbitrary timeouts. This improves code reliability and prevents
  hangs or deadlocks.
repository: neondatabase/neon
label: Concurrency
language: Python
comments_count: 2
repository_stars: 19015
---

When handling concurrent operations, prefer completion signals and proper thread management over arbitrary timeouts. This improves code reliability and prevents hangs or deadlocks.

For waiting on asynchronous processes:
- Instead of arbitrary timeouts that can cause flaky tests:
  ```python
  # Avoid this
  wait_until(lambda: assert_condition(), timeout=120)
  
  # Prefer this
  env.storage_controller.reconcile_until_idle()
  wait_until(lambda: assert_condition())
  ```

For operations that might block indefinitely:
- Use thread pools to prevent the main execution thread from hanging:
  ```python
  # Instead of potentially blocking code
  ps.restart()  # Could hang waiting for active status
  
  # Use a ThreadPoolExecutor for potentially blocking operations
  with concurrent.futures.ThreadPoolExecutor() as executor:
      future = executor.submit(ps.restart)
      # Continue execution or implement proper timeout handling
  ```

These patterns ensure that your concurrent code is more predictable, testable, and less prone to timing-dependent issues.