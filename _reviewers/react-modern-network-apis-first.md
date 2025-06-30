---
title: Modern network APIs first
description: Prioritize modern web streaming APIs for network communication while
  providing fallback strategies for browser compatibility. When implementing network
  features, prefer modern interfaces like WebSocketStream over legacy alternatives,
  but document necessary polyfills or fallback mechanisms for environments lacking
  support.
repository: facebook/react
label: Networking
language: Javascript
comments_count: 2
repository_stars: 236852
---

Prioritize modern web streaming APIs for network communication while providing fallback strategies for browser compatibility. When implementing network features, prefer modern interfaces like WebSocketStream over legacy alternatives, but document necessary polyfills or fallback mechanisms for environments lacking support.

For example, when implementing WebSocket-based communication:

```javascript
// Preferred approach using modern WebSocketStream API
if (typeof WebSocketStream === 'function') {
  const requestId = crypto.randomUUID(); // Generate correlation ID
  const { writable, readable } = await new WebSocketStream(url);
  // Use web streams for communication
} else {
  // Provide fallback implementation or documentation for
  // browsers without WebSocketStream support (Safari, Firefox)
  // Consider using polyfills or alternative transport protocols
}
```

When creating networked features that need to work across both browser and server environments, clearly document the API differences and ensure your implementation accounts for platform-specific behaviors.

## Discussions

### [packages/react-server-dom-webpack/src/client/ReactFlightDOMClientBrowser.js](https://github.com/facebook/react/pull/33627)

```javascript
export type Options = {
  callServer?: CallServerCallback,
  debugChannel?: {writable?: WritableStream, ...},
```

**Discussion:**

- **sebmarkbage:** Notably the client is currently only included in the Browser builds. I guess in theory it could be useful to have a live connection between servers too.  This accepts a `writable: WritableStream` which is the shape that is provided by the modern [WebSocketStream](https://developer.mozilla.org/en-US/docs/Web/API/WebSocketStream) API. It's aligned with all our other modern usages for browsers - Web Streams.  Unfortunately WebSocketStream is not available in Safari or Firefox so those need a polyfill. I didn't add support for the more widely supported [`WebSocket` API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) since that would also affect the `readable` directly where we stopped [supporting the XHR shape](https://github.com/facebook/react/pull/26827). So this is just left up to user space for now to polyfill or use a different transport protocol.  Ironically the `WebSocket` shape is commonly in Node.js and it has similar but not exact shape as Node Streams so I added support for the Web shape of `WebSocket` in Node.

### [fixtures/flight/src/index.js](https://github.com/facebook/react/pull/33627)

```javascript
}

async function hydrateApp() {
  const {root, returnValue, formState} = await createFromFetch(
    fetch('/', {
      headers: {
        Accept: 'text/x-component',
      },
    }),
    {
      callServer,
      findSourceMapURL,
    }
  );
  let response;
  if (
    process.env.NODE_ENV === 'development' &&
    typeof WebSocketStream === 'function'
  ) {
    const requestId = crypto.randomUUID();
```

**Discussion:**

- **sebmarkbage:** This is used to associate the WebSocket request with the fetch request.  In theory, this system can work with multiple development servers. E.g. it's resilient to the server restarting (loses the connection) which is nice.  However, if you have multiple servers that might respond to the socket request vs the fetch, you end up with different servers answering.  Another approach would be to also just make the RSC request through the WebSocket.

