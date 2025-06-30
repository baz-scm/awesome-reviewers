---
title: Deferred loading strategy
description: Implement a consistent strategy for deferred object loading in caching
  systems, with clear rules for when to cache objects for later retrieval versus when
  to emit them eagerly. Track deferred objects to optimize serialization decisions
  and prevent redundant processing.
repository: facebook/react
label: Caching
language: Javascript
comments_count: 2
repository_stars: 236852
---

Implement a consistent strategy for deferred object loading in caching systems, with clear rules for when to cache objects for later retrieval versus when to emit them eagerly. Track deferred objects to optimize serialization decisions and prevent redundant processing.

When implementing deferred loading mechanisms:
1. Maintain accurate tracking of deferred objects through appropriate data structures
2. Establish clear object limits to control memory usage
3. Document the lifecycle of cached resources, particularly when they are released
4. Consider previous serialization decisions when encountering the same object multiple times

```javascript
// Example implementation
function serializeDeferredObject(request, value) {
  const deferredDebugObjects = request.deferredDebugObjects;
  if (deferredDebugObjects !== null) {
    // This client supports a long lived connection. We can assign this object
    // an ID to be lazy loaded later.
    // This keeps the connection alive until we ask for it or release it.
    
    // Check if we've seen this object before
    const deferredId = deferredDebugObjects.existing.get(value);
    if (deferredId !== undefined) {
      // Determine whether to emit eagerly based on current object limits
      if (counter.objectLimit > 0) {
        // Emit eagerly when limits allow
        return serializeEagerObject(request, value, deferredId);
      }
      // Otherwise keep using the deferred reference
      return deferredId;
    }
  }
  // Handle non-deferrable case
}
```

## Discussions

### [packages/react-server/src/ReactFlightServer.js](https://github.com/facebook/react/pull/33627)

```javascript
return '$S' + name;
}

function serializeLimitedObject(): string {
function serializeDeferredObject(
  request: Request,
  value: ReactClientReference | string,
): string {
  const deferredDebugObjects = request.deferredDebugObjects;
  if (deferredDebugObjects !== null) {
    // This client supports a long lived connection. We can assign this object
    // an ID to be lazy loaded later.
    // This keeps the connection alive until we ask for it or retain it.
```

**Discussion:**

- **unstubbable:** ```suggestion     // This keeps the connection alive until we ask for it or release it. ``` Right?

### [packages/react-server/src/ReactFlightServer.js](https://github.com/facebook/react/pull/33627)

```javascript
if (counter.objectLimit <= 0 && !doNotLimit.has(value)) {
      // We've reached our max number of objects to serialize across the wire so we serialize this
      // as a marker so that the client can error when this is accessed by the console.
      return serializeLimitedObject();
      // as a marker so that the client can error or lazy load thiswhen accessed by the console.
      return serializeDeferredObject(request, value);
    }

    counter.objectLimit--;

    const deferredDebugObjects = request.deferredDebugObjects;
    if (deferredDebugObjects !== null) {
      const deferredId = deferredDebugObjects.existing.get(value);
      // We earlier deferred this same object. We're now going to eagerly emit it so let's emit it
      // at the same ID that we already used to refer to it.
```

**Discussion:**

- **unstubbable:** Why do we emit eagerly when we see it twice?
- **sebmarkbage:** We only get here if we have passed the objectLimit check above. Either because something else with a high limit also wrote this object or because we're now asking for it from the client.  If there's still an object limit being enforced we wouldn't get here no matter how many times we see the same object.

