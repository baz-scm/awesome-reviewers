---
title: Thread safety first
description: 'When implementing features that may run concurrently, always ensure
  thread safety using appropriate synchronization mechanisms:


  1. Use thread-safe context variables for isolating execution contexts:'
repository: crewaiinc/crewai
label: Concurrency
language: Python
comments_count: 3
repository_stars: 33945
---

When implementing features that may run concurrently, always ensure thread safety using appropriate synchronization mechanisms:

1. Use thread-safe context variables for isolating execution contexts:
   ```python
   # Good: Using contextvars-based solutions for thread isolation
   ctx = baggage.set_baggage(...)  # Uses contextvars internally for thread safety
   ```

2. Protect shared mutable state with locks:
   ```python
   # Good: Adding locks to prevent race conditions
   _lock: Lock = threading.Lock()
   
   def singleton_method(self):
       with self._lock:
           # Access or modify shared state safely
   ```

3. Implement thread-based timeouts efficiently:
   ```python
   # Better: Simple thread-based timeout pattern
   thread = threading.Thread(target=target, daemon=True)
   thread.start()
   thread.join(timeout=timeout)
   
   if thread.is_alive():
       # Handle timeout case
   ```

These patterns help prevent hard-to-debug race conditions, ensure consistent behavior in concurrent environments, and make code more maintainable by clearly indicating thread safety considerations.