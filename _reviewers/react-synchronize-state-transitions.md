---
title: Synchronize state transitions
description: When implementing asynchronous operations, ensure that state transitions
  complete fully before proceeding with dependent operations. This prevents race conditions
  where subsequent code might interact with intermediate or inconsistent states, leading
  to unpredictable behavior.
repository: facebook/react
label: Concurrency
language: Javascript
comments_count: 2
repository_stars: 236851
---

When implementing asynchronous operations, ensure that state transitions complete fully before proceeding with dependent operations. This prevents race conditions where subsequent code might interact with intermediate or inconsistent states, leading to unpredictable behavior.

In React components or data processing pipelines, verify that a component or data chunk has reached its intended state before triggering the next operation in the sequence:

```javascript
// Potentially unsafe approach
function processStream(chunk, nextOperation) {
  initiateStateTransition(chunk);
  // Race condition potential: nextOperation may run before state transition completes
  nextOperation(chunk);
}

// Safer approach
function processStream(chunk, nextOperation) {
  initiateStateTransition(chunk).then(() => {
    // Only proceed when transition is complete
    nextOperation(chunk);
  });
}
```

This pattern is especially important when:
1. Multiple asynchronous operations depend on each other
2. The order of execution affects the outcome
3. Debugging or logging requires accurate state representation

## Discussions

## thread:2173885122

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

## thread:2159425945

@@ -266,7 +266,11 @@ ReactPromise.prototype.then = function <T>(
       initializeModuleChunk(chunk);
       break;
   }
-  if (__DEV__ && enableAsyncDebugInfo) {
+  if (
+    __DEV__ &&
+    enableAsyncDebugInfo &&
+    (typeof resolve !== 'function' || !(resolve: any).isReactInternalListener)

### sebmarkbage

The microtask here means that cycles don't resolve synchronously which means that console logs can miss them. This is not the only thing that can be async though. If you console log a client reference that hasn't loaded yet you get the same problem.

In the future, we should really make sure that the debug info can be parsed async while retaining console log order. 

