---
title: Modern network API compatibility
description: When implementing WebSocket or stream-based communication, prioritize
  cross-browser and cross-platform compatibility. Modern APIs like WebSocketStream
  provide elegant solutions but require fallback strategies for browsers without native
  support.
repository: facebook/react
label: Networking
language: Javascript
comments_count: 2
repository_stars: 236861
---

When implementing WebSocket or stream-based communication, prioritize cross-browser and cross-platform compatibility. Modern APIs like WebSocketStream provide elegant solutions but require fallback strategies for browsers without native support.

Consider these practices:
- Document browser compatibility requirements for networking code
- Implement appropriate polyfills or fallbacks for less-supported features
- Use correlation IDs when coordinating between different connection types
- Test resilience during server restarts or in multi-server environments

Example:
```javascript
// Connection setup with browser compatibility consideration
async function setupConnection() {
  if (typeof WebSocketStream === 'function') {
    // Modern approach using WebSocketStream
    const requestId = crypto.randomUUID();
    return connectWithWebSocketStream(requestId);
  } else {
    // Fallback for browsers without WebSocketStream support
    return connectWithTraditionalFetch({
      headers: {
        Accept: 'text/x-component',
      },
    });
  }
}

// Ensure correlation between requests
function connectWithWebSocketStream(requestId) {
  // Use requestId to correlate this connection with other requests
  // ...
}
```

This approach maintains code quality while addressing real-world networking constraints across different runtime environments.


[
  {
    "discussion_id": "2162851827",
    "pr_number": 33627,
    "pr_file": "packages/react-server-dom-webpack/src/client/ReactFlightDOMClientBrowser.js",
    "created_at": "2025-06-24T02:40:43+00:00",
    "commented_code": "export type Options = {\n  callServer?: CallServerCallback,\n  debugChannel?: {writable?: WritableStream, ...},",
    "repo_full_name": "facebook/react",
    "discussion_comments": [
      {
        "comment_id": "2162851827",
        "repo_full_name": "facebook/react",
        "pr_number": 33627,
        "pr_file": "packages/react-server-dom-webpack/src/client/ReactFlightDOMClientBrowser.js",
        "discussion_id": "2162851827",
        "commented_code": "@@ -42,12 +43,31 @@ type CallServerCallback = <A, T>(string, args: A) => Promise<T>;\n \n export type Options = {\n   callServer?: CallServerCallback,\n+  debugChannel?: {writable?: WritableStream, ...},",
        "comment_created_at": "2025-06-24T02:40:43+00:00",
        "comment_author": "sebmarkbage",
        "comment_body": "Notably the client is currently only included in the Browser builds. I guess in theory it could be useful to have a live connection between servers too.\r\n\r\nThis accepts a `writable: WritableStream` which is the shape that is provided by the modern [WebSocketStream](https://developer.mozilla.org/en-US/docs/Web/API/WebSocketStream) API. It's aligned with all our other modern usages for browsers - Web Streams.\r\n\r\nUnfortunately WebSocketStream is not available in Safari or Firefox so those need a polyfill. I didn't add support for the more widely supported [`WebSocket` API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) since that would also affect the `readable` directly where we stopped [supporting the XHR shape](https://github.com/facebook/react/pull/26827). So this is just left up to user space for now to polyfill or use a different transport protocol.\r\n\r\nIronically the `WebSocket` shape is commonly in Node.js and it has similar but not exact shape as Node Streams so I added support for the Web shape of `WebSocket` in Node.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2162866847",
    "pr_number": 33627,
    "pr_file": "fixtures/flight/src/index.js",
    "created_at": "2025-06-24T03:00:03+00:00",
    "commented_code": "}\n\nasync function hydrateApp() {\n  const {root, returnValue, formState} = await createFromFetch(\n    fetch('/', {\n      headers: {\n        Accept: 'text/x-component',\n      },\n    }),\n    {\n      callServer,\n      findSourceMapURL,\n    }\n  );\n  let response;\n  if (\n    process.env.NODE_ENV === 'development' &&\n    typeof WebSocketStream === 'function'\n  ) {\n    const requestId = crypto.randomUUID();",
    "repo_full_name": "facebook/react",
    "discussion_comments": [
      {
        "comment_id": "2162866847",
        "repo_full_name": "facebook/react",
        "pr_number": 33627,
        "pr_file": "fixtures/flight/src/index.js",
        "discussion_id": "2162866847",
        "commented_code": "@@ -42,17 +42,43 @@ function Shell({data}) {\n }\n \n async function hydrateApp() {\n-  const {root, returnValue, formState} = await createFromFetch(\n-    fetch('/', {\n-      headers: {\n-        Accept: 'text/x-component',\n-      },\n-    }),\n-    {\n-      callServer,\n-      findSourceMapURL,\n-    }\n-  );\n+  let response;\n+  if (\n+    process.env.NODE_ENV === 'development' &&\n+    typeof WebSocketStream === 'function'\n+  ) {\n+    const requestId = crypto.randomUUID();",
        "comment_created_at": "2025-06-24T03:00:03+00:00",
        "comment_author": "sebmarkbage",
        "comment_body": "This is used to associate the WebSocket request with the fetch request.\r\n\r\nIn theory, this system can work with multiple development servers. E.g. it's resilient to the server restarting (loses the connection) which is nice.\r\n\r\nHowever, if you have multiple servers that might respond to the socket request vs the fetch, you end up with different servers answering.\r\n\r\nAnother approach would be to also just make the RSC request through the WebSocket.",
        "pr_file_module": null
      }
    ]
  }
]
