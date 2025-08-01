---
title: Ensure operation completion safety
description: 'In concurrent code, ensure that operations complete safely before proceeding
  to prevent race conditions and data corruption. This applies to several scenarios:'
repository: LMCache/LMCache
label: Concurrency
language: Python
comments_count: 7
repository_stars: 3800
---

In concurrent code, ensure that operations complete safely before proceeding to prevent race conditions and data corruption. This applies to several scenarios:

**Lock Management**: Use context managers instead of manual lock acquisition to guarantee proper cleanup:
```python
# Good - automatic cleanup
with self.manager_lock:
    prefetch_task = self.prefetch_tasks.pop(key)

# Avoid - manual lock management
self.manager_lock.acquire()
prefetch_task = self.prefetch_tasks.pop(key)
self.manager_lock.release()
```

**Async Operation Safety**: When data integrity is critical, ensure async operations complete before proceeding:
```python
# Good - synchronous when safety is needed
memory_obj.tensor.copy_(hidden_states)

# Risky - async copy without synchronization
memory_obj.tensor.copy_(hidden_states, non_blocking=True)
```

**Atomic File Operations**: Prevent race conditions in file operations using temporary files and atomic renames:
```python
# Good - atomic operation
tmp_path = path + ".tmp"
with open(tmp_path, 'wb') as f:
    f.write(data)
os.rename(tmp_path, path)  # Atomic on most filesystems
```

**Reference Counting Timing**: Ensure reference counting operations happen at the right time relative to object usage:
```python
# Ensure backend consumes object before counting down
backend.submit_put_task(key, obj)
# Backend should call ref_count_down() after consumption
```

**Stream Synchronization**: Use proper stream synchronization for CUDA operations:
```python
put_stream = torch.cuda.Stream()
if kv_chunk.device != torch.cpu:
    put_stream.wait_stream(torch.cuda.default_stream(kv_chunk.device))
```

The key principle is to identify critical sections where partial completion could cause issues and ensure these operations are atomic or properly synchronized.