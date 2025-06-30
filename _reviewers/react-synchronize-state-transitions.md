---
title: Synchronize state transitions
description: When implementing asynchronous operations, ensure that state transitions
  are fully completed before allowing dependent operations to proceed. This prevents
  race conditions where subsequent operations might make incorrect assumptions about
  the system state.
repository: facebook/react
label: Concurrency
language: Javascript
comments_count: 2
repository_stars: 236852
---

When implementing asynchronous operations, ensure that state transitions are fully completed before allowing dependent operations to proceed. This prevents race conditions where subsequent operations might make incorrect assumptions about the system state.

For example, when processing streams or iterables of data:
```javascript
// AVOID: This may cause race conditions
function resolveNextChunk(chunks, id, stream) {
  const nextChunk = createStreamChunk(stream);
  chunks.set(id, nextChunk);
  processNextChunkImmediately(); // Danger: May execute before state is stable
}

// BETTER: Ensure state is properly synchronized
function resolveNextChunk(chunks, id, stream) {
  const nextChunk = createStreamChunk(stream);
  chunks.set(id, nextChunk);
  
  // Only proceed when chunk is in non-pending state
  if (nextChunk.status !== PENDING) {
    processNextChunkSafely();
  } else {
    // Register a callback to run after state transition completes
    nextChunk.onStateTransitionComplete(() => {
      processNextChunkSafely();
    });
  }
}
```

Additionally, use consistent patterns for aborting or canceling asynchronous operations to maintain predictable concurrency behavior across the codebase. This reduces the risk of race conditions, resource leaks, and unexpected system behavior.

## Discussions

## packages/react-client/src/ReactFlightClient.js, https://github.com/facebook/react/pull/33665

@@ -2229,6 +2250,22 @@ function resolveStream<T: ReadableStream | $AsyncIterable<any, any, void>>(
     chunks.set(id, createInitializedStreamChunk(response, stream, controller));
     return;
   }
+  if (__DEV__) {
+    const blockedDebugInfo = chunk._blockedDebugInfo;
+    if (blockedDebugInfo != null) {
+      // If we're blocked on debug info, wait until it has loaded before we resolve.
+      const unblock = resolveStream.bind(
+        null,
+        response,
+        id,
+        stream,
+        controller,
+      );
+      blockedDebugInfo.then(unblock, unblock);

### sebmarkbage

I don't think this is safe because the chunk needs to enter a non-pending state before the next chunk is resolved. Otherwise the next chunk doesn't know it's a stream entry.

## packages/react-server/src/ReactFlightServer.js, https://github.com/facebook/react/pull/33633

@@ -1110,16 +1103,18 @@ function serializeAsyncIterable(
       iterator.throw(reason).then(error, error);
     }
   }
-  function abortIterable(reason: mixed) {
-    if (aborted) {
+  function abortIterable() {
+    if (streamTask.status !== PENDING) {
       return;
     }
-    aborted = true;
-    request.abortListeners.delete(abortIterable);
+    const signal = request.cacheController.signal;
+    signal.removeEventListener('abort', abortIterable);
+    const reason = signal.reason;
     if (enableHalt && request.type === PRERENDER) {
-      request.pendingChunks--;
+      haltTask(streamTask, request);
+      request.abortableTasks.delete(streamTask);
     } else {
-      erroredTask(request, streamTask, reason);
+      erroredTask(request, streamTask, signal.reason);

### unstubbable

Why aren't we using `abortTask` here? (same question for streams)

### sebmarkbage

Yea I noticed that. We probably should.  

### sebmarkbage

I think the reason we didn't originally is because we don't have access to the `errorId` here so it would be different copy of the error object regardless.

If we tried to share it with the root, we'd need some way to signal back that we used the shared one with is more complicated.

I'll leave this as an issue for now.

