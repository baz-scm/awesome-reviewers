---
title: Guard every async boundary
description: Every promise chain, detached ("fire-and-forget") call, timer callback,
  and event/stream listener (socket `message`, child-process `stdin`/`exit`, write-stream
  errors) must have an explicit error handler. Code outside a `try`/`catch` that rejects
  or throws in one of these contexts does not propagate to a surrounding handler —
  it becomes an unhandled...
repository: "cline/cline\r\n"
label: Error Handling
language: TypeScript
comments_count: 7
repository_stars: 70946
---

Every promise chain, detached ("fire-and-forget") call, timer callback, and event/stream listener (socket `message`, child-process `stdin`/`exit`, write-stream errors) must have an explicit error handler. Code outside a `try`/`catch` that rejects or throws in one of these contexts does not propagate to a surrounding handler — it becomes an unhandled rejection or an uncaught exception in a listener, which can crash or exit the whole host process depending on the runtime's unhandled-rejection policy, not just fail the one operation.

Concretely:
- Never write `promise.then(onSuccess)` without a paired failure handler. Note that `promise.then(onSuccess, onError)` does **not** catch an exception thrown *inside* `onSuccess`; use `promise.then(onSuccess).catch(onError)` whenever the success branch itself can throw.
- Any call that can itself throw during cleanup or teardown (`kill()`, `dispose()`, closing a socket) must be wrapped in `try`/`catch` and routed through the same failure path as the original error, rather than being allowed to escape as a second, unhandled error.
- When parsing untrusted input off the wire (`JSON.parse` on a socket frame, a subprocess message), wrap the parse in `try`/`catch`, and on failure fail that specific operation/connection with a real, diagnostic cause (not a generic message) instead of letting the exception bubble out of the listener.
- A store/log/telemetry write that can itself throw (e.g., inside an `onError` callback) must be wrapped so a misbehaving sink cannot turn a handled failure into a second, unhandled one; retry state should be preserved before the fallible callback runs.

```ts
// Bad: an exception thrown inside attach() becomes an unhandled rejection
promise.then(attach, onError);

// Good: covers both a rejected promise and a throw inside attach()
promise.then(attach).catch(onError);

// Bad: kill() can throw synchronously; nothing here catches it
handle.kill();

// Good: route the failure through the same error path
try {
	handle.kill();
} catch (error) {
	handle.fail(error instanceof Error ? error : new Error(String(error)));
}

// Bad: a malformed frame throws inside the listener and can kill the process
ws.addEventListener("message", (event) => {
	const frame = JSON.parse(String(event.data));
	handleFrame(frame);
});

// Good: contain the failure and close the connection with a real cause
ws.addEventListener("message", (event) => {
	let frame;
	try {
		frame = JSON.parse(String(event.data));
	} catch (error) {
		this.lastCloseError = new TransportError("unparseable_frame", String(error));
		ws.close();
		return;
	}
	handleFrame(frame);
});
```

Treat any new `.then(...)`, detached `void asyncFn()`, or listener registration as incomplete until its failure path is explicit — this is as important to review as the happy path.