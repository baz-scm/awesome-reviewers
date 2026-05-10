---
title: Thread-safe lifecycle isolation
description: When changing concurrency/background execution, ensure (a) state is isolated
  per thread/consumer/instance, and (b) shutdown/cleanup and exception signaling are
  coordinated with explicit synchronization.
repository: celery/celery
label: Concurrency
language: Python
comments_count: 9
repository_stars: 28464
---

When changing concurrency/background execution, ensure (a) state is isolated per thread/consumer/instance, and (b) shutdown/cleanup and exception signaling are coordinated with explicit synchronization.

**Standards**
1) **Isolate per-thread/per-consumer resources**
   - Don’t rely on global event loops.
   - Don’t store `threading.local()` (or thread-specific state) as a module/class attribute; prefer per-`Celery`/backend instance or initialize thread-local fields during `start()`.

2) **Coordinate shutdown with Events and correct lifecycle ownership**
   - Use `threading.Event()`/similar primitives to signal stop/shutdown.
   - Put resource cleanup in the component that actually owns the resource, respecting shutdown order (avoid clearing shared timers/hub resources too early).

3) **Make exception propagation race-safe**
   - If a background loop can error, store the exception and synchronize visibility (e.g., set a shutdown event in `finally`, then read the exception after the event).

4) **Always close/reconnect thread-bound resources**
   - PubSub/socket-like resources should be explicitly closed when reconnecting or tearing down; deadlocks often come from missed/uncertain teardown.

**Example pattern**
```python
import threading

class BackgroundWorker:
    def __init__(self):
        self._stop = threading.Event()
        self._shutdown = threading.Event()
        self._exc = None
        self._thread_local = threading.local()  # instance-scoped

    def start(self):
        if getattr(self._thread_local, "started", False):
            return
        self._thread_local.started = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        try:
            while not self._stop.is_set():
                # do work...
                pass
        except Exception as e:
            self._exc = e
        finally:
            # single point to publish shutdown state
            self._shutdown.set()
            # close thread-bound resources here

    def stop(self):
        self._stop.set()
        self._shutdown.wait(timeout=10)
        if self._exc is not None:
            raise self._exc
```

**Code-review checklist**
- Is any loop/thread state stored globally or as class-level `threading.local()`? (Fix to per-instance/per-thread.)
- Are stop/shutdown signals coordinated with `Event`s, and is shared state read only after synchronization?
- Are cleanup actions performed by the correct owner component in the correct shutdown phase?
- Are thread-bound resources explicitly closed/recreated to avoid deadlocks/races?
- Do the changes avoid high-risk wrapping/monkey-patching of concurrency/QoS internals unless necessary and well-tested?