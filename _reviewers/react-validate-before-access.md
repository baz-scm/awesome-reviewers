---
title: Validate before access
description: Always validate that objects are not null before performing operations
  on them, and provide clear, specific error messages when null values are encountered
  unexpectedly. This helps prevent null reference errors and improves debuggability.
repository: facebook/react
label: Null Handling
language: Javascript
comments_count: 2
repository_stars: 236852
---

Always validate that objects are not null before performing operations on them, and provide clear, specific error messages when null values are encountered unexpectedly. This helps prevent null reference errors and improves debuggability.

Example:
```javascript
// Good practice
function processRequest(request) {
  const deferredObjects = request.deferredDebugObjects;
  if (deferredObjects === null) {
    throw new Error(
      "Operation cannot be performed on a request without initialized debug objects. This is a bug in the application."
    );
  }
  // Proceed with operations on deferredObjects safely
}

// Avoid
function processRequest(request) {
  // This might throw cryptic "Cannot read property of null" error
  const items = request.deferredDebugObjects.retained.get(id);
}
```

When throwing errors for null values, include context about why the value shouldn't be null and what might have caused the issue. This makes troubleshooting easier and clarifies expected preconditions for functions.

## Discussions

## packages/react-server/src/ReactFlightServer.js, https://github.com/facebook/react/pull/33627

@@ -5254,3 +5307,82 @@ export function abort(request: Request, reason: mixed): void {
     fatalError(request, error);
   }
 }
+
+function fromHex(str: string): number {
+  return parseInt(str, 16);
+}
+
+export function resolveDebugMessage(request: Request, message: string): void {
+  if (!__DEV__) {
+    // These errors should never make it into a build so we don't need to encode them in codes.json
+    // eslint-disable-next-line react-internal/prod-error-codes
+    throw new Error(
+      'resolveDebugMessage should never be called in production mode. This is a bug in React.',
+    );
+  }
+  const deferredDebugObjects = request.deferredDebugObjects;
+  if (deferredDebugObjects === null) {
+    throw new Error(
+      "resolveDebugMessage/closeDebugChannel not be called for a Request that wasn't kept alive. This is a bug in React.",
+    );
+  }
+  // This function lets the client ask for more data lazily through the debug channel.
+  const command = message.charCodeAt(0);
+  const ids = message.slice(2).split(',').map(fromHex);
+  switch (command) {
+    case 82 /* "R" */:
+      // Release IDs
+      for (let i = 0; i < ids.length; i++) {
+        const id = ids[i];
+        const retainedValue = deferredDebugObjects.retained.get(id);
+        if (retainedValue !== undefined) {
+          // We're no longer blocked on this. We won't emit it.
+          request.pendingChunks--;
+          deferredDebugObjects.retained.delete(id);
+          deferredDebugObjects.existing.delete(retainedValue);
+          enqueueFlush(request);
+        }
+      }
+      break;
+    case 81 /* "Q" */:
+      // Query IDs
+      for (let i = 0; i < ids.length; i++) {
+        const id = ids[i];
+        const retainedValue = deferredDebugObjects.retained.get(id);
+        if (retainedValue !== undefined) {
+          // If we still have this object, and haven't emitted it before, emit it on the stream.
+          const counter = {objectLimit: 10};
+          emitOutlinedDebugModelChunk(request, id, counter, retainedValue);
+          enqueueFlush(request);
+        }
+      }
+      break;
+    default:
+      throw new Error(
+        'Unknown command. The debugChannel was not wired up properly.',
+      );
+  }
+}
+
+export function closeDebugChannel(request: Request): void {
+  if (!__DEV__) {
+    // These errors should never make it into a build so we don't need to encode them in codes.json
+    // eslint-disable-next-line react-internal/prod-error-codes
+    throw new Error(
+      'closeDebugChannel should never be called in production mode. This is a bug in React.',
+    );
+  }
+  // This clears all remaining deferred objects, potentially resulting in the completion of the Request.
+  const deferredDebugObjects = request.deferredDebugObjects;
+  if (deferredDebugObjects === null) {
+    throw new Error(
+      "resolveDebugMessage/closeDebugChannel not be called for a Request that wasn't kept alive. This is a bug in React.",

### unstubbable

```suggestion
      "resolveDebugMessage/closeDebugChannel should not be called for a Request that wasn't kept alive. This is a bug in React.",
```

## packages/react-server/src/ReactFlightServer.js, https://github.com/facebook/react/pull/33627

@@ -5254,3 +5307,82 @@ export function abort(request: Request, reason: mixed): void {
     fatalError(request, error);
   }
 }
+
+function fromHex(str: string): number {
+  return parseInt(str, 16);
+}
+
+export function resolveDebugMessage(request: Request, message: string): void {
+  if (!__DEV__) {
+    // These errors should never make it into a build so we don't need to encode them in codes.json
+    // eslint-disable-next-line react-internal/prod-error-codes
+    throw new Error(
+      'resolveDebugMessage should never be called in production mode. This is a bug in React.',
+    );
+  }
+  const deferredDebugObjects = request.deferredDebugObjects;
+  if (deferredDebugObjects === null) {
+    throw new Error(
+      "resolveDebugMessage/closeDebugChannel not be called for a Request that wasn't kept alive. This is a bug in React.",

### unstubbable

```suggestion
      "resolveDebugMessage/closeDebugChannel should not be called for a Request that wasn't kept alive. This is a bug in React.",
```

