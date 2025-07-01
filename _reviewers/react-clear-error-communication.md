---
title: Clear error communication
description: Ensure all error messages and comments about error handling are clear,
  complete, and grammatically correct. This helps developers quickly understand error
  scenarios, improves debugging efficiency, and prevents confusion when troubleshooting
  issues.
repository: facebook/react
label: Error Handling
language: Javascript
comments_count: 2
repository_stars: 236861
---

Ensure all error messages and comments about error handling are clear, complete, and grammatically correct. This helps developers quickly understand error scenarios, improves debugging efficiency, and prevents confusion when troubleshooting issues.

When writing error messages:
- Include all necessary words for grammatical completeness
- Clearly describe what went wrong
- Provide context about why the error occurred
- Suggest remedial action when possible

For example, instead of:
```javascript
throw new Error(
  "resolveDebugMessage/closeDebugChannel not be called for a Request that wasn't kept alive. This is a bug in React.",
);
```

Write:
```javascript
throw new Error(
  "resolveDebugMessage/closeDebugChannel should not be called for a Request that wasn't kept alive. This is a bug in React.",
);
```

The same principles apply to comments that document error handling logic:
- Use proper grammar and clear language
- Explain the purpose and context of error handling code
- Help future developers understand edge cases and failure scenarios


[
  {
    "discussion_id": "2164787211",
    "pr_number": 33632,
    "pr_file": "packages/react-server/src/ReactFlightServer.js",
    "created_at": "2025-06-24T19:56:48+00:00",
    "commented_code": "}\n}\n\nfunction forwardDebugInfoFromAbortedTask(request: Request, task: Task): void {\n  // If we a task is aborted, we can still include as much debug info as we can from the",
    "repo_full_name": "facebook/react",
    "discussion_comments": [
      {
        "comment_id": "2164787211",
        "repo_full_name": "facebook/react",
        "pr_number": 33632,
        "pr_file": "packages/react-server/src/ReactFlightServer.js",
        "discussion_id": "2164787211",
        "commented_code": "@@ -4679,6 +4686,74 @@ function forwardDebugInfoFromCurrentContext(\n   }\n }\n \n+function forwardDebugInfoFromAbortedTask(request: Request, task: Task): void {\n+  // If we a task is aborted, we can still include as much debug info as we can from the",
        "comment_created_at": "2025-06-24T19:56:48+00:00",
        "comment_author": "unstubbable",
        "comment_body": "```suggestion\r\n  // If a task is aborted, we can still include as much debug info as we can from the\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2163550194",
    "pr_number": 33627,
    "pr_file": "packages/react-server/src/ReactFlightServer.js",
    "created_at": "2025-06-24T10:17:54+00:00",
    "commented_code": "fatalError(request, error);\n  }\n}\n\nfunction fromHex(str: string): number {\n  return parseInt(str, 16);\n}\n\nexport function resolveDebugMessage(request: Request, message: string): void {\n  if (!__DEV__) {\n    // These errors should never make it into a build so we don't need to encode them in codes.json\n    // eslint-disable-next-line react-internal/prod-error-codes\n    throw new Error(\n      'resolveDebugMessage should never be called in production mode. This is a bug in React.',\n    );\n  }\n  const deferredDebugObjects = request.deferredDebugObjects;\n  if (deferredDebugObjects === null) {\n    throw new Error(\n      \"resolveDebugMessage/closeDebugChannel not be called for a Request that wasn't kept alive. This is a bug in React.\",\n    );\n  }\n  // This function lets the client ask for more data lazily through the debug channel.\n  const command = message.charCodeAt(0);\n  const ids = message.slice(2).split(',').map(fromHex);\n  switch (command) {\n    case 82 /* \"R\" */:\n      // Release IDs\n      for (let i = 0; i < ids.length; i++) {\n        const id = ids[i];\n        const retainedValue = deferredDebugObjects.retained.get(id);\n        if (retainedValue !== undefined) {\n          // We're no longer blocked on this. We won't emit it.\n          request.pendingChunks--;\n          deferredDebugObjects.retained.delete(id);\n          deferredDebugObjects.existing.delete(retainedValue);\n          enqueueFlush(request);\n        }\n      }\n      break;\n    case 81 /* \"Q\" */:\n      // Query IDs\n      for (let i = 0; i < ids.length; i++) {\n        const id = ids[i];\n        const retainedValue = deferredDebugObjects.retained.get(id);\n        if (retainedValue !== undefined) {\n          // If we still have this object, and haven't emitted it before, emit it on the stream.\n          const counter = {objectLimit: 10};\n          emitOutlinedDebugModelChunk(request, id, counter, retainedValue);\n          enqueueFlush(request);\n        }\n      }\n      break;\n    default:\n      throw new Error(\n        'Unknown command. The debugChannel was not wired up properly.',\n      );\n  }\n}\n\nexport function closeDebugChannel(request: Request): void {\n  if (!__DEV__) {\n    // These errors should never make it into a build so we don't need to encode them in codes.json\n    // eslint-disable-next-line react-internal/prod-error-codes\n    throw new Error(\n      'closeDebugChannel should never be called in production mode. This is a bug in React.',\n    );\n  }\n  // This clears all remaining deferred objects, potentially resulting in the completion of the Request.\n  const deferredDebugObjects = request.deferredDebugObjects;\n  if (deferredDebugObjects === null) {\n    throw new Error(\n      \"resolveDebugMessage/closeDebugChannel not be called for a Request that wasn't kept alive. This is a bug in React.\",",
    "repo_full_name": "facebook/react",
    "discussion_comments": [
      {
        "comment_id": "2163550194",
        "repo_full_name": "facebook/react",
        "pr_number": 33627,
        "pr_file": "packages/react-server/src/ReactFlightServer.js",
        "discussion_id": "2163550194",
        "commented_code": "@@ -5254,3 +5307,82 @@ export function abort(request: Request, reason: mixed): void {\n     fatalError(request, error);\n   }\n }\n+\n+function fromHex(str: string): number {\n+  return parseInt(str, 16);\n+}\n+\n+export function resolveDebugMessage(request: Request, message: string): void {\n+  if (!__DEV__) {\n+    // These errors should never make it into a build so we don't need to encode them in codes.json\n+    // eslint-disable-next-line react-internal/prod-error-codes\n+    throw new Error(\n+      'resolveDebugMessage should never be called in production mode. This is a bug in React.',\n+    );\n+  }\n+  const deferredDebugObjects = request.deferredDebugObjects;\n+  if (deferredDebugObjects === null) {\n+    throw new Error(\n+      \"resolveDebugMessage/closeDebugChannel not be called for a Request that wasn't kept alive. This is a bug in React.\",\n+    );\n+  }\n+  // This function lets the client ask for more data lazily through the debug channel.\n+  const command = message.charCodeAt(0);\n+  const ids = message.slice(2).split(',').map(fromHex);\n+  switch (command) {\n+    case 82 /* \"R\" */:\n+      // Release IDs\n+      for (let i = 0; i < ids.length; i++) {\n+        const id = ids[i];\n+        const retainedValue = deferredDebugObjects.retained.get(id);\n+        if (retainedValue !== undefined) {\n+          // We're no longer blocked on this. We won't emit it.\n+          request.pendingChunks--;\n+          deferredDebugObjects.retained.delete(id);\n+          deferredDebugObjects.existing.delete(retainedValue);\n+          enqueueFlush(request);\n+        }\n+      }\n+      break;\n+    case 81 /* \"Q\" */:\n+      // Query IDs\n+      for (let i = 0; i < ids.length; i++) {\n+        const id = ids[i];\n+        const retainedValue = deferredDebugObjects.retained.get(id);\n+        if (retainedValue !== undefined) {\n+          // If we still have this object, and haven't emitted it before, emit it on the stream.\n+          const counter = {objectLimit: 10};\n+          emitOutlinedDebugModelChunk(request, id, counter, retainedValue);\n+          enqueueFlush(request);\n+        }\n+      }\n+      break;\n+    default:\n+      throw new Error(\n+        'Unknown command. The debugChannel was not wired up properly.',\n+      );\n+  }\n+}\n+\n+export function closeDebugChannel(request: Request): void {\n+  if (!__DEV__) {\n+    // These errors should never make it into a build so we don't need to encode them in codes.json\n+    // eslint-disable-next-line react-internal/prod-error-codes\n+    throw new Error(\n+      'closeDebugChannel should never be called in production mode. This is a bug in React.',\n+    );\n+  }\n+  // This clears all remaining deferred objects, potentially resulting in the completion of the Request.\n+  const deferredDebugObjects = request.deferredDebugObjects;\n+  if (deferredDebugObjects === null) {\n+    throw new Error(\n+      \"resolveDebugMessage/closeDebugChannel not be called for a Request that wasn't kept alive. This is a bug in React.\",",
        "comment_created_at": "2025-06-24T10:17:54+00:00",
        "comment_author": "unstubbable",
        "comment_body": "```suggestion\r\n      \"resolveDebugMessage/closeDebugChannel should not be called for a Request that wasn't kept alive. This is a bug in React.\",\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
