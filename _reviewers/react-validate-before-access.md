---
title: Validate before access
description: Always validate that objects are in their expected state before accessing
  their properties to prevent runtime errors. Include explicit null/undefined checks
  and provide clear error messages when validations fail.
repository: facebook/react
label: Null Handling
language: Javascript
comments_count: 3
repository_stars: 236851
---

Always validate that objects are in their expected state before accessing their properties to prevent runtime errors. Include explicit null/undefined checks and provide clear error messages when validations fail.

Good practice:
```javascript
function resolveDebugMessage(request: Request, message: string): void {
  const deferredDebugObjects = request.deferredDebugObjects;
  if (deferredDebugObjects === null) {
    throw new Error(
      "resolveDebugMessage should not be called for a Request that wasn't kept alive. This is a bug in React."
    );
  }
  // Safe to access deferredDebugObjects after validation
  // ...
}
```

Bad practice:
```javascript
function parseModel(response, json) {
  // Assuming key === '' means this is the root model without validation
  isParsingRootModel = key === '';
  // This assumption could fail on nested objects with empty keys
  // ...
}
```

When accessing properties of objects, especially those from external sources or that might have been modified, use safe access patterns like `hasOwnProperty.call()` or first check if the property exists. This helps avoid undefined behavior and makes your code more robust against unexpected inputs.

## Discussions

## thread:1951676728

@@ -3393,6 +3410,7 @@ function parseModel<T>(response: Response, json: UninitializedModel): T {
 function createFromJSONCallback(response: Response) {
   // $FlowFixMe[missing-this-annot]
   return function (key: string, value: JSONValue) {
+    isParsingRootModel = key === '';

### sebmarkbage

We can't assume that an empty string key is the root since it may also be on nested objects. What's the implication of that?

### unstubbable

Hmm, we were already using the check here:
https://github.com/facebook/react/blob/192555bb0ed88db30f91c58651c421f178f90384/packages/react-client/src/ReactFlightClient.js#L983-L987
But I guess you're right, it could also be an explicit empty key in some object.

## thread:2163550194

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

## thread:2160459438

@@ -4066,6 +4080,34 @@ function renderDebugModel(
       return Array.from((value: any));
     }
 
+    const proto = getPrototypeOf(value);
+    if (proto !== ObjectPrototype && proto !== null) {
+      const object: Object = value;
+      const instanceDescription: Object = Object.create(null);
+      for (const propName in object) {
+        if (hasOwnProperty.call(value, propName) || isGetter(proto, propName)) {
+          // We intentionally invoke getters on the prototype to read any enumerable getters.
+          instanceDescription[propName] = object[propName];

### unstubbable

I'm a bit concerned that this might trigger unwanted side effects, like the getters on the "exotic" promises in Next.js.

### sebmarkbage

Yea, but for them to be discovered they have to be enumerable so the trick is to make them non-enumerable.

Getters are non-enumerable by default when defined by syntax and when added with `defineProperty`.

If anything the concerning bit might be the enumerability trap but that's a concern regardless.

