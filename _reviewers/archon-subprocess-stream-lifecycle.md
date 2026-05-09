---
title: Subprocess stream lifecycle
description: When you stream a subprocess’s stdout/stderr into an async generator,
  treat process exit, stream end/close, abort, and timeout escalation as concurrent
  events that can race.
repository: coleam00/Archon
label: Concurrency
language: TypeScript
comments_count: 2
repository_stars: 21089
---

When you stream a subprocess’s stdout/stderr into an async generator, treat process exit, stream end/close, abort, and timeout escalation as concurrent events that can race.

**Coding standard**
1. **Finalize on stream close/flush, not only on `exit`.** The “last output” might still be buffered when `exit` fires. Listen for stream `close`/`end` (or the streams’ close) and only then yield the final `result`/exit chunk.
2. **Coordinate producers/consumer with a single queue.** Use a shared async event queue so stdout/stderr/exit/abort events are serialized for the generator.
3. **Make timeouts and escalation timers deterministic.** Store timer IDs, clear them before rescheduling and in a cleanup path, and `unref()` escalation timers so they don’t keep the worker alive.
4. **Regression-test the race.** Add a test where `exit` happens before stdout/stderr stream end to ensure the final chunk is yielded only after buffers are flushed.

**Example pattern (simplified)**
```ts
// shared queue
const { push, next } = makeEventQueue();
let processExited = false;
let stdoutClosed = false;
let stderrClosed = false;

const killProcess = (reason: string) => {
  if (processExited) return;
  child.kill('SIGTERM');

  // escalation timer: track + clear + unref
  if (sigkillTimer) clearTimeout(sigkillTimer);
  sigkillTimer = setTimeout(() => {
    if (!processExited) child.kill('SIGKILL');
  }, 2000);
  sigkillTimer.unref();
};

pipeLinesToQueue(child.stdout!, 'stdout', push);
pipeLinesToQueue(child.stderr!, 'stderr', push);

child.once('exit', (code, signal) => {
  processExited = true;
  push({ kind: 'exit', code, signal });
});

// Finalize only when streams are closed/flushed
child.stdout?.once('close', () => { stdoutClosed = true; push({ kind: 'stdout_close' } as any); });
child.stderr?.once('close', () => { stderrClosed = true; push({ kind: 'stderr_close' } as any); });

// consumer: drain events, then yield result when both close + exit known
// (implementation depends on your result-yield strategy)
```

Applying this prevents lost tail output, double-yields, and subtle leaks/hangs caused by concurrent lifecycle events and uncleared timers.