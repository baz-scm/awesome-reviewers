---
title: Protect shared state
description: When mutable state (like dictionaries, lists, or counters) is accessed
  from multiple threads or concurrent tasks, use appropriate synchronization mechanisms
  to prevent race conditions. Unprotected access to shared state can lead to data
  corruption, inconsistent behavior, and hard-to-debug issues.
repository: vllm-project/vllm
label: Concurrency
language: Python
comments_count: 3
repository_stars: 51730
---

When mutable state (like dictionaries, lists, or counters) is accessed from multiple threads or concurrent tasks, use appropriate synchronization mechanisms to prevent race conditions. Unprotected access to shared state can lead to data corruption, inconsistent behavior, and hard-to-debug issues.

For example, wrap dictionary operations with locks:

```python
# Unsafe - race condition if called concurrently:
self._reqs_to_send[req_id] = some_value
del self._reqs_to_send[req_id]

# Safe with lock protection:
self._reqs_to_send_lock = threading.Lock()  # Initialize in constructor

# Later in code:
with self._reqs_to_send_lock:
    self._reqs_to_send[req_id] = some_value
    del self._reqs_to_send[req_id]
```

In asynchronous code, also be careful with shared variables that might be modified by interleaved tasks. Instead of relying on shared context, pass necessary context through the call stack:

```python
# Unsafe with shared state in async code:
self._set_tokenizer(tokenizer)  # Could be modified by another task before use

# Safe - pass explicitly through call stack:
result = await self._process_with_tokenizer(tokenizer, input_text)
```