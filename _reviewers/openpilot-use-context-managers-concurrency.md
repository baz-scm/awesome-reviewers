---
title: use context managers concurrency
description: When working with concurrent operations involving shared resources or
  processes, use context managers and explicit synchronization to ensure proper cleanup
  and thread safety. This prevents resource leaks, race conditions, and ensures graceful
  shutdown even when operations are interrupted.
repository: commaai/openpilot
label: Concurrency
language: Python
comments_count: 5
repository_stars: 58214
---

When working with concurrent operations involving shared resources or processes, use context managers and explicit synchronization to ensure proper cleanup and thread safety. This prevents resource leaks, race conditions, and ensures graceful shutdown even when operations are interrupted.

For process management, wrap subprocess operations in context managers instead of relying on atexit handlers:

```python
# Instead of atexit.register()
with ProcessManager() as pm:
    xvfb_proc = pm.start_process(xvfb_cmd, env)
    ui_proc = pm.start_process(ui_cmd, env)
    # processes automatically cleaned up on exit
```

For shared resources accessed by multiple threads, use explicit locking:

```python
class AudioProcessor:
    def __init__(self):
        self.lock = threading.Lock()  # Add a lock for thread safety
        self.sound_data = []
    
    def process_audio(self, data):
        with self.lock:
            self.sound_data.append(data)
```

When adding concurrency to existing APIs, maintain backward compatibility by encapsulating threading details within the implementation rather than exposing them to consumers. This allows you to improve responsiveness (like preventing UI freezing) without breaking existing code that depends on the original synchronous interface.