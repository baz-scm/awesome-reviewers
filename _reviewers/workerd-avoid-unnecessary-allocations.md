---
title: avoid unnecessary allocations
description: Minimize object creation and memory copying operations to improve performance.
  Cache and reuse objects when possible, use buffer views instead of copying data,
  and avoid creating temporary objects that will be immediately discarded.
repository: cloudflare/workerd
label: Performance Optimization
language: TypeScript
comments_count: 5
repository_stars: 6989
---

Minimize object creation and memory copying operations to improve performance. Cache and reuse objects when possible, use buffer views instead of copying data, and avoid creating temporary objects that will be immediately discarded.

Key practices:
- Cache expensive objects like Readers instead of creating new ones on each call
- Use buffer views (`new Uint8Array(buf.buffer, buf.byteOffset, buf.byteLength)`) instead of copying data twice
- Avoid creating objects that are immediately overwritten or discarded
- Use efficient concatenation methods like `Buffer.concat()` instead of manual array operations

Example of inefficient allocation:
```js
// Creates unnecessary ReadableStream that gets overwritten
let stream = this.bindingsResponse.body || new ReadableStream();
if (options?.encoding === 'base64') {
  stream = stream.pipeThrough(createBase64EncoderTransformStream());
}

// Creates new Reader on every call
const reader = this._stream.getReader();
```

Example of optimized allocation:
```js
// Only create ReadableStream when needed
const stream = options?.encoding === 'base64' 
  ? (this.bindingsResponse.body || new ReadableStream()).pipeThrough(createBase64EncoderTransformStream())
  : (this.bindingsResponse.body || new ReadableStream());

// Cache and reuse Reader
if (!this._cachedReader) {
  this._cachedReader = this._stream.getReader();
}
```