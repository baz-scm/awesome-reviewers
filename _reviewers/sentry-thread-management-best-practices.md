---
title: Thread management best practices
description: 'When working with threads or thread pools in concurrent code, follow
  these practices to improve reliability and debuggability:


  1. **Always name your threads and thread pools** using the `thread_name_prefix`
  parameter. This makes debugging and monitoring much easier when issues arise.'
repository: getsentry/sentry
label: Concurrency
language: Python
comments_count: 4
repository_stars: 41297
---

When working with threads or thread pools in concurrent code, follow these practices to improve reliability and debuggability:

1. **Always name your threads and thread pools** using the `thread_name_prefix` parameter. This makes debugging and monitoring much easier when issues arise.

```python
# Good
executor = ThreadPoolExecutor(max_workers=10, thread_name_prefix="data-processor")

# Good
thread = threading.Thread(name="result-sender", target=process_results)

# Avoid - unnamed threads make debugging difficult
executor = ThreadPoolExecutor(max_workers=10)
```

2. **Set appropriate timeouts** for blocking operations like thread joins and future results to prevent indefinitely blocking the main process:

```python
# Good - explicit timeout prevents hanging
thread.join(timeout=1.0)
future.result(timeout=5.0)

# Avoid - may block indefinitely
thread.join()
```

3. **Use daemon threads** when the thread should terminate when the main process exits and shouldn't block application shutdown:

```python
# Good for service threads that can terminate with the program
thread = threading.Thread(target=background_task, daemon=True)
```

4. **Be careful with timeouts in concurrent contexts** - understand how your concurrency primitives handle timeouts. For example, when using `as_completed`, the timeout is already handled and doesn't need to be repeated in the `future.result()` call.

Following these practices will help avoid common threading pitfalls like application hang during shutdown, thread leaks, and difficult-to-debug concurrency issues.