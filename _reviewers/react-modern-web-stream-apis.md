---
title: Modern web stream APIs
description: Use modern Web Stream APIs for network communications when available,
  particularly for WebSocket connections, while ensuring proper cross-browser compatibility
  and connection management.
repository: facebook/react
label: Networking
language: Javascript
comments_count: 2
repository_stars: 236851
---

Use modern Web Stream APIs for network communications when available, particularly for WebSocket connections, while ensuring proper cross-browser compatibility and connection management.

When implementing network functionality:
1. Prefer modern APIs like WebSocketStream that align with Web Streams for consistency
2. Consider browser compatibility and provide appropriate fallbacks when needed
3. Implement proper request association for WebSocket connections

Example:
```javascript
// Preferred approach using WebSocketStream when available
if (typeof WebSocketStream === 'function') {
  const requestId = crypto.randomUUID();
  const webSocketStream = new WebSocketStream(url);
  // Associate with related fetch requests
  const { readable, writable } = await webSocketStream.connection;
  // Use the stream...
} else {
  // Fallback for browsers without WebSocketStream support
  // Consider polyfill or alternative approach
}
```

This approach ensures your networking code leverages modern APIs while maintaining compatibility across different environments and properly managing connections between related requests.

## Discussions

## thread:2162851827

@@ -42,12 +43,31 @@ type CallServerCallback = <A, T>(string, args: A) => Promise<T>;
 
 export type Options = {
   callServer?: CallServerCallback,
+  debugChannel?: {writable?: WritableStream, ...},

### sebmarkbage

Notably the client is currently only included in the Browser builds. I guess in theory it could be useful to have a live connection between servers too.

This accepts a `writable: WritableStream` which is the shape that is provided by the modern [WebSocketStream](https://developer.mozilla.org/en-US/docs/Web/API/WebSocketStream) API. It's aligned with all our other modern usages for browsers - Web Streams.

Unfortunately WebSocketStream is not available in Safari or Firefox so those need a polyfill. I didn't add support for the more widely supported [`WebSocket` API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) since that would also affect the `readable` directly where we stopped [supporting the XHR shape](https://github.com/facebook/react/pull/26827). So this is just left up to user space for now to polyfill or use a different transport protocol.

Ironically the `WebSocket` shape is commonly in Node.js and it has similar but not exact shape as Node Streams so I added support for the Web shape of `WebSocket` in Node.

## thread:2162866847

@@ -42,17 +42,43 @@ function Shell({data}) {
 }
 
 async function hydrateApp() {
-  const {root, returnValue, formState} = await createFromFetch(
-    fetch('/', {
-      headers: {
-        Accept: 'text/x-component',
-      },
-    }),
-    {
-      callServer,
-      findSourceMapURL,
-    }
-  );
+  let response;
+  if (
+    process.env.NODE_ENV === 'development' &&
+    typeof WebSocketStream === 'function'
+  ) {
+    const requestId = crypto.randomUUID();

### sebmarkbage

This is used to associate the WebSocket request with the fetch request.

In theory, this system can work with multiple development servers. E.g. it's resilient to the server restarting (loses the connection) which is nice.

However, if you have multiple servers that might respond to the socket request vs the fetch, you end up with different servers answering.

Another approach would be to also just make the RSC request through the WebSocket.

