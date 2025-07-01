---
title: Document caching strategies
description: Always clearly document the decision logic for caching strategies, especially
  when determining whether objects should be eagerly loaded or deferred for lazy loading.
  This helps maintain consistent performance optimization and makes the caching behavior
  predictable for other developers.
repository: facebook/react
label: Caching
language: Javascript
comments_count: 2
repository_stars: 236861
---

Always clearly document the decision logic for caching strategies, especially when determining whether objects should be eagerly loaded or deferred for lazy loading. This helps maintain consistent performance optimization and makes the caching behavior predictable for other developers.

For example, when implementing object caching with deduplication:

```javascript
// Good: Document the caching behavior and decision logic
function serializeObject(request, value) {
  const cachedObjects = request.cachedObjects;
  if (cachedObjects !== null) {
    // If we've seen this object before, reuse the cached reference
    // to optimize memory usage and maintain reference equality
    const cachedId = cachedObjects.existing.get(value);
    if (cachedId !== undefined) {
      // We eagerly emit the object when:
      // 1. The object limit is no longer being enforced
      // 2. The object is specifically requested by the client
      // Otherwise, we return the cached reference
      if (request.objectLimit <= 0 || request.explicitlyRequested.has(value)) {
        return generateEagerReference(cachedId);
      }
      return generateCachedReference(cachedId);
    }
  }
  
  // First time seeing this object, decide whether to cache it
  // based on size, access patterns, and application needs
  return registerNewObject(request, value);
}
```

When implementing caching systems, also ensure that tests clearly demonstrate the expected behavior of shared references and deduplication, making it obvious when objects are meant to be reference-equal after deserialization.


[
  {
    "discussion_id": "1948264753",
    "pr_number": 32316,
    "pr_file": "packages/react-server-dom-webpack/src/__tests__/ReactFlightDOMBrowser-test.js",
    "created_at": "2025-02-09T23:14:28+00:00",
    "commented_code": "expect(container.innerHTML).toBe('{\"foo\":1}{\"foo\":1}');\n  });\n\n  it('should resolve deduped references in maps used in client component props', async () => {\n    const ClientComponent = clientExports(function ClientComponent({\n      shared,\n      map,\n    }) {\n      return JSON.stringify({shared, map: Array.from(map)});",
    "repo_full_name": "facebook/react",
    "discussion_comments": [
      {
        "comment_id": "1948264753",
        "repo_full_name": "facebook/react",
        "pr_number": 32316,
        "pr_file": "packages/react-server-dom-webpack/src/__tests__/ReactFlightDOMBrowser-test.js",
        "discussion_id": "1948264753",
        "commented_code": "@@ -533,6 +533,42 @@ describe('ReactFlightDOMBrowser', () => {\n     expect(container.innerHTML).toBe('{\"foo\":1}{\"foo\":1}');\n   });\n \n+  it('should resolve deduped references in maps used in client component props', async () => {\n+    const ClientComponent = clientExports(function ClientComponent({\n+      shared,\n+      map,\n+    }) {\n+      return JSON.stringify({shared, map: Array.from(map)});",
        "comment_created_at": "2025-02-09T23:14:28+00:00",
        "comment_author": "eps1lon",
        "comment_body": "Is `shared` supposed to be equal to `map.get(42)` on the Client? We should probably make that clear in the test.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2163572667",
    "pr_number": 33627,
    "pr_file": "packages/react-server/src/ReactFlightServer.js",
    "created_at": "2025-06-24T10:29:17+00:00",
    "commented_code": "if (counter.objectLimit <= 0 && !doNotLimit.has(value)) {\n      // We've reached our max number of objects to serialize across the wire so we serialize this\n      // as a marker so that the client can error when this is accessed by the console.\n      return serializeLimitedObject();\n      // as a marker so that the client can error or lazy load thiswhen accessed by the console.\n      return serializeDeferredObject(request, value);\n    }\n\n    counter.objectLimit--;\n\n    const deferredDebugObjects = request.deferredDebugObjects;\n    if (deferredDebugObjects !== null) {\n      const deferredId = deferredDebugObjects.existing.get(value);\n      // We earlier deferred this same object. We're now going to eagerly emit it so let's emit it\n      // at the same ID that we already used to refer to it.",
    "repo_full_name": "facebook/react",
    "discussion_comments": [
      {
        "comment_id": "2163572667",
        "repo_full_name": "facebook/react",
        "pr_number": 33627,
        "pr_file": "packages/react-server/src/ReactFlightServer.js",
        "discussion_id": "2163572667",
        "commented_code": "@@ -4058,12 +4091,25 @@ function renderDebugModel(\n \n     if (counter.objectLimit <= 0 && !doNotLimit.has(value)) {\n       // We've reached our max number of objects to serialize across the wire so we serialize this\n-      // as a marker so that the client can error when this is accessed by the console.\n-      return serializeLimitedObject();\n+      // as a marker so that the client can error or lazy load thiswhen accessed by the console.\n+      return serializeDeferredObject(request, value);\n     }\n \n     counter.objectLimit--;\n \n+    const deferredDebugObjects = request.deferredDebugObjects;\n+    if (deferredDebugObjects !== null) {\n+      const deferredId = deferredDebugObjects.existing.get(value);\n+      // We earlier deferred this same object. We're now going to eagerly emit it so let's emit it\n+      // at the same ID that we already used to refer to it.",
        "comment_created_at": "2025-06-24T10:29:17+00:00",
        "comment_author": "unstubbable",
        "comment_body": "Why do we emit eagerly when we see it twice?",
        "pr_file_module": null
      },
      {
        "comment_id": "2164214557",
        "repo_full_name": "facebook/react",
        "pr_number": 33627,
        "pr_file": "packages/react-server/src/ReactFlightServer.js",
        "discussion_id": "2163572667",
        "commented_code": "@@ -4058,12 +4091,25 @@ function renderDebugModel(\n \n     if (counter.objectLimit <= 0 && !doNotLimit.has(value)) {\n       // We've reached our max number of objects to serialize across the wire so we serialize this\n-      // as a marker so that the client can error when this is accessed by the console.\n-      return serializeLimitedObject();\n+      // as a marker so that the client can error or lazy load thiswhen accessed by the console.\n+      return serializeDeferredObject(request, value);\n     }\n \n     counter.objectLimit--;\n \n+    const deferredDebugObjects = request.deferredDebugObjects;\n+    if (deferredDebugObjects !== null) {\n+      const deferredId = deferredDebugObjects.existing.get(value);\n+      // We earlier deferred this same object. We're now going to eagerly emit it so let's emit it\n+      // at the same ID that we already used to refer to it.",
        "comment_created_at": "2025-06-24T14:40:30+00:00",
        "comment_author": "sebmarkbage",
        "comment_body": "We only get here if we have passed the objectLimit check above. Either because something else with a high limit also wrote this object or because we're now asking for it from the client.\r\n\r\nIf there's still an object limit being enforced we wouldn't get here no matter how many times we see the same object.",
        "pr_file_module": null
      }
    ]
  }
]
