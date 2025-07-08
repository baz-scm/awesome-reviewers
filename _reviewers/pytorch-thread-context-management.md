---
title: Thread context management
description: Always explicitly set required thread context and state rather than assuming
  inheritance from parent threads or other concurrent processes. In multithreaded
  and distributed environments, assumptions about shared state can lead to subtle
  bugs, race conditions, and incorrect behavior.
repository: pytorch/pytorch
label: Concurrency
language: Python
comments_count: 3
repository_stars: 91345
---

Always explicitly set required thread context and state rather than assuming inheritance from parent threads or other concurrent processes. In multithreaded and distributed environments, assumptions about shared state can lead to subtle bugs, race conditions, and incorrect behavior.

For example, when setting device context in a multithreaded environment:

```python
# Incorrect: Assuming device context is inherited
def _pin_memory_loop(in_queue, out_queue, done_event, device):
    # This might not work as expected in a different thread
    process_data(in_queue)

# Correct: Explicitly set device context in each thread
def _pin_memory_loop(in_queue, out_queue, done_event, device):
    # Set device context explicitly in this thread
    torch.accelerator.set_device_index(torch.accelerator.current_device_index())
    process_data(in_queue)
```

Similarly, be careful about assumptions regarding process groups in distributed computing. Each component should clearly document and validate its threading model and required context. Use proper synchronization mechanisms like barriers when operations across threads depend on each other's completion.