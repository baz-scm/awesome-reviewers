---
title: Modern network API standards
description: When implementing networking functionality, prioritize modern Web APIs
  that align with current standards and existing codebase patterns, while providing
  appropriate fallbacks for cross-browser and cross-environment compatibility.
repository: facebook/react
label: Networking
language: Javascript
comments_count: 2
repository_stars: 236852
---

When implementing networking functionality, prioritize modern Web APIs that align with current standards and existing codebase patterns, while providing appropriate fallbacks for cross-browser and cross-environment compatibility.

Specifically:
- Use modern Web APIs like WebSocketStream that align with Web Streams for consistency
- Document browser compatibility concerns and polyfill requirements
- Consider connection resilience for service disruptions (e.g., server restarts)
- Use appropriate identifiers to associate related requests across protocols

Example:
```javascript
// Good: Using modern WebSocketStream with fallback considerations
if (
  process.env.NODE_ENV === 'development' &&
  typeof WebSocketStream === 'function'
) {
  // Modern approach with WebSocketStream
  const requestId = crypto.randomUUID();
  // Use requestId to associate with other requests
  // ...
} else {
  // Fallback for environments without WebSocketStream
  // Consider documenting polyfill requirements
}

// Options that accept modern API shapes
export type Options = {
  callServer?: CallServerCallback,
  debugChannel?: {writable?: WritableStream, ...},
  // Other options...
};
```

This approach ensures your networking code leverages modern capabilities while maintaining necessary compatibility across browsers and environments.

## Discussions

## packages/react-server-dom-webpack/src/client/ReactFlightDOMClientBrowser.js, https://github.com/facebook/react/pull/33627

@@ -42,12 +43,31 @@ type CallServerCallback = <A, T>(string, args: A) => Promise<T>;
 
 export type Options = {
   callServer?: CallServerCallback,
+  debugChannel?: {writable?: WritableStream, ...},

### sebmarkbage

Notably the client is currently only included in the Browser builds. I guess in theory it could be useful to have a live connection between servers too.

This accepts a `writable: WritableStream` which is the shape that is provided by the modern [WebSocketStream](https://developer.mozilla.org/en-US/docs/Web/API/WebSocketStream) API. It's aligned with all our other modern usages for browsers - Web Streams.

Unfortunately WebSocketStream is not available in Safari or Firefox so those need a polyfill. I didn't add support for the more widely supported [`WebSocket` API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) since that would also affect the `readable` directly where we stopped [supporting the XHR shape](https://github.com/facebook/react/pull/26827). So this is just left up to user space for now to polyfill or use a different transport protocol.

Ironically the `WebSocket` shape is commonly in Node.js and it has similar but not exact shape as Node Streams so I added support for the Web shape of `WebSocket` in Node.

## fixtures/flight/src/index.js, https://github.com/facebook/react/pull/33627

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

