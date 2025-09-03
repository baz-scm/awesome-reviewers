---
title: Replace polling with events
description: Replace busy-wait polling loops with event-driven async patterns using
  asyncio.Event() or similar synchronization primitives. Polling loops that continuously
  check state variables waste CPU cycles and block the event loop, while event-driven
  patterns allow the thread to yield control until the condition is actually met.
repository: browser-use/browser-use
label: Concurrency
language: Python
comments_count: 3
repository_stars: 69139
---

Replace busy-wait polling loops with event-driven async patterns using asyncio.Event() or similar synchronization primitives. Polling loops that continuously check state variables waste CPU cycles and block the event loop, while event-driven patterns allow the thread to yield control until the condition is actually met.

Look for patterns like:
```python
# Avoid: Busy-wait polling
while self.state.paused:
    await asyncio.sleep(0.1)  # Still wastes cycles checking every 100ms
```

Replace with event-driven patterns:
```python
# Prefer: Event-driven waiting
self._pause_event = asyncio.Event()

# In the waiting code:
await self._pause_event.wait()  # Blocks until event is set, no polling

# In the control code:
def pause(self):
    self.state.paused = True
    self._pause_event.clear()

def resume(self):
    self.state.paused = False
    self._pause_event.set()
```

This approach eliminates CPU spinning, allows proper async task isolation (each task can have its own events), and removes the need for redundant state variables when the event itself serves as the synchronization mechanism. Consider removing duplicate state tracking when the event primitive provides the same information.