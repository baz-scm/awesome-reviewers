---
title: Choose appropriate synchronization
description: Select the correct synchronization mechanism based on your execution
  context and avoid unnecessary synchronization overhead. In async contexts with coroutines,
  locks are often unnecessary since coroutines run cooperatively in a single thread.
  Use `asyncio.Lock()` for async contexts and `threading.Lock()` for multi-threaded
  scenarios. When bridging sync and...
repository: strands-agents/sdk-python
label: Concurrency
language: Python
comments_count: 7
repository_stars: 4044
---

Select the correct synchronization mechanism based on your execution context and avoid unnecessary synchronization overhead. In async contexts with coroutines, locks are often unnecessary since coroutines run cooperatively in a single thread. Use `asyncio.Lock()` for async contexts and `threading.Lock()` for multi-threaded scenarios. When bridging sync and async code with threads, ensure proper context variable propagation and use daemon threads for background tasks.

Key guidelines:
- **Async contexts**: Coroutines run cooperatively, so locks are usually unnecessary unless coordinating with external threads
- **Mixed contexts**: Use `asyncio.Lock()` when coordinating async tasks, `threading.Lock()` for thread coordination
- **Thread creation**: Use daemon threads for background tasks and ensure proper exception propagation
- **Context variables**: Copy context when creating threads to maintain variable scope

Example of proper lock selection:
```python
# Async context - lock usually unnecessary
async def process_nodes_async(self, nodes):
    # Coroutines run cooperatively, no race conditions
    for node in nodes:
        self.state.completed_nodes.add(node)

# Mixed async/thread context - use asyncio.Lock
class GraphExecutor:
    def __init__(self):
        self._lock = asyncio.Lock()  # For async task coordination
    
    async def execute_parallel(self, nodes):
        async with self._lock:  # Only if truly needed
            # Critical section
            pass

# Thread context - use threading.Lock  
class FileManager:
    def __init__(self):
        self._lock = threading.RLock()  # For thread coordination
    
    def write_file(self, data):
        with self._lock:
            # Thread-safe file operations
            pass
```

Before adding synchronization, verify you actually have a race condition. Many async operations don't require explicit locking due to the cooperative nature of coroutines.