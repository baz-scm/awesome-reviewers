---
title: Handle async failures explicitly
description: 'Treat every asynchronous operation''s failure path as part of its contract,
  not an afterthought. This standard covers two recurring classes of bugs:


  1. **Never leave a promise, stream, or child process without an attached failure
  handler.** A `.then(onSuccess)` with no second argument or `.catch`, a `child.stdin`/socket
  with no `"error"` listener, or a...'
repository: cline/cline#$(sleep 4)
label: Error Handling
language: TypeScript
comments_count: 18
repository_stars: 70978
---

Treat every asynchronous operation's failure path as part of its contract, not an afterthought. This standard covers two recurring classes of bugs:

1. **Never leave a promise, stream, or child process without an attached failure handler.** A `.then(onSuccess)` with no second argument or `.catch`, a `child.stdin`/socket with no `"error"` listener, or a `kill()`/`dispose()` call whose rejection is ignored all become unhandled rejections or uncaught exceptions that can crash the host process. Always pair success handling with explicit failure handling:
   ```ts
   // Bad: exceptions inside attach(), or a rejected kill(), escape uncaught.
   void loadMxc().then(attach, onSpawnError);

   // Good: every branch, including failures thrown during the success path,
   // is funneled through one handler.
   void loadMxc().then(attach).catch(onSpawnError);
   child.stdin.on("error", (err) => handle.fail(toError(err)));
   ```
   The same applies to `JSON.parse` on data read from a socket/wire: wrap it so a malformed frame closes the connection and rejects pending work with a real cause, instead of throwing inside an event listener.

2. **Never let a failure silently present as success.** Check the actual outcome (`finishReason`, exit code, thrown error, `isError` flag) before reporting a status, persisting a checkpoint, or returning a result object. Don't catch-and-ignore a write/commit failure and continue as if it succeeded, don't classify a result as "completed" without checking for an `"error"` finish reason, and don't let a generic fallback (e.g. retry classification, data truncation bypass) override a more specific failure signal. When an operation partially completes and then fails, preserve the partial/original result and surface the failure — don't discard the evidence of what actually happened or let a "recovery" step silently replace a failing outcome with the illusion of a successful one.

Before merging code with async control flow, ask: "If this specific call rejects or throws, where does that error go, and does any status/telemetry field I'm about to set still reflect the truth?" Add a test that forces the failure path and asserts both that nothing escapes unhandled and that the reported status/error matches reality.</description>
