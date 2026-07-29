---
title: Nonblocking Concurrency Rules
description: 'Establish a single concurrency standard: in async code, never block
  the event loop; in multi-thread/state-machine code, make ownership and cancellation
  atomic; and in cleanup/shutdown, use bounded, interrupt-friendly paths.'
repository: nousresearch/hermes-agent
label: Concurrency
language: Python
comments_count: 14
repository_stars: 221948
---

Establish a single concurrency standard: in async code, never block the event loop; in multi-thread/state-machine code, make ownership and cancellation atomic; and in cleanup/shutdown, use bounded, interrupt-friendly paths.

1) Keep async nonblocking
- Any `subprocess.run`, CPU-heavy work (ffprobe/ffmpeg, compressors, summary generation), synchronous SDK calls, or blocking I/O must be offloaded.
- Pattern:
```py
# BAD: blocks event loop
result = subprocess.run([...], timeout=60)

# GOOD
result = await asyncio.to_thread(subprocess.run, [...], timeout=60)
# or
result = await adapter._run_blocking(func, *args)
```

2) Re-check cancellation/flags after waits
- If a worker can be paused in `Event.wait()` (or similar), it must re-check the controlling mode/flag at every boundary where it could restart capture/playback/processing.
- Pattern:
```py
await voice_done.wait()
if cli_ref._voice_continuous is False:
    return  # cancel boundary
```

3) Lock/claim correctly; snapshot atomically
- When multiple pieces of state must be consistent (e.g., status + payload), take the same lock for a single snapshot.
- When there is a single owner (wake-word listener, shared callback transport, adapter connection-local services), implement a real lease/claim/release so late callers can’t steal delivery.

4) Shutdown/cleanup must be bounded and interrupt-friendly
- Never perform blocking cleanup (e.g., `shutdown(wait=True)`) before the code path that needs to deliver an interrupt/watchdog action.
- Prefer bounded waits or non-blocking cancellation first:
```py
# BAD if interrupt must run promptly
pool.shutdown(wait=True, cancel_futures=True)

# BETTER: cancel first, then bounded wait, then allow interrupt to proceed
pool.shutdown(wait=False, cancel_futures=True)
# or wait with a timeout in your own logic
```

5) Add regression coverage for the real concurrency boundary
- For cross-thread queueing (e.g., `put_threadsafe()`), tests must involve a real worker thread, not only same-loop calls.
- For ownership/leases and cross-process locks, add OS-process regressions (where supported) to validate the intended guard behavior.