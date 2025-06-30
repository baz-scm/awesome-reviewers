---
title: Consistent code style
description: 'Maintain consistent and readable code style throughout the codebase
  by following these practices:


  1. Use named constants instead of magic numbers to improve code readability and
  maintainability:'
repository: axios/axios
label: Code Style
language: Javascript
comments_count: 2
repository_stars: 107146
---

Maintain consistent and readable code style throughout the codebase by following these practices:

1. Use named constants instead of magic numbers to improve code readability and maintainability:

```javascript
// Instead of this:
bytes: 4,

// Use this:
const BYTES_PER_CHUNK = 4;
bytes: BYTES_PER_CHUNK,
```

2. Follow consistent formatting conventions:
   - Add proper spacing in object literals `{ value }` instead of `{value}`
   - Use semicolons consistently at the end of statements
   - Use meaningful variable names (use `_` for intentionally unused variables)

3. Write descriptive comments that explain the purpose or reason for code blocks rather than just adding eslint directives:

```javascript
// Instead of:
} catch (e) {
  // eslint-disable-next-line no-empty
}

// Use this:
} catch (_) {
  // name property might be read-only; safely ignored
}
```

Following these style conventions makes code more maintainable and easier for team members to read and understand.

## Discussions

## thread:2083900694

@@ -0,0 +1,400 @@
+import assert from 'assert';
+import {
+  startHTTPServer,
+  stopHTTPServer,
+  LOCAL_SERVER_URL,
+  setTimeoutAsync,
+  makeReadableStream,
+  generateReadable,
+  makeEchoStream
+} from '../../helpers/server.js';
+import axios from '../../../index.js';
+import stream from "stream";
+import {AbortController} from "abortcontroller-polyfill/dist/cjs-ponyfill.js";
+import util from "util";
+
+const pipelineAsync = util.promisify(stream.pipeline);
+
+const undiciAxios = axios.create({
+  baseURL: LOCAL_SERVER_URL,
+  adapter: 'undici'
+});
+
+let server;
+
+describe('supports undici with nodejs', function () {
+
+  afterEach(async function () {
+    await stopHTTPServer(server);
+
+    server = null;
+  });
+
+  describe('responses', async () => {
+    it(`should support text response type`, async () => {
+      const originalData = 'my data';
+
+      server = await startHTTPServer((req, res) => res.end(originalData));
+
+      const {data} = await undiciAxios.get('/', {
+        responseType: 'text'
+      });
+
+      assert.deepStrictEqual(data, originalData);
+    });
+
+    it(`should support arraybuffer response type`, async () => {
+      const originalData = 'my data';
+
+      server = await startHTTPServer((req, res) => res.end(originalData));
+
+      const {data} = await undiciAxios.get('/', {
+        responseType: 'arraybuffer'
+      });
+
+      assert.deepStrictEqual(data, Uint8Array.from(await new TextEncoder().encode(originalData)).buffer);
+    });
+
+    it(`should support blob response type`, async () => {
+      const originalData = 'my data';
+
+      server = await startHTTPServer((req, res) => res.end(originalData));
+
+      const {data} = await undiciAxios.get('/', {
+        responseType: 'blob'
+      });
+
+      assert.deepStrictEqual(data, new Blob([originalData]));
+    });
+
+    it(`should support stream response type`, async () => {
+      const originalData = 'my data';
+
+      server = await startHTTPServer((req, res) => res.end(originalData));
+
+      const {data} = await undiciAxios.get('/', {
+        responseType: 'stream'
+      });
+
+      assert.ok(data instanceof ReadableStream, 'data is not instanceof ReadableStream');
+
+      let response = new Response(data);
+
+      assert.deepStrictEqual(await response.text(), originalData);
+    });
+
+    it(`should support formData response type`, async function () {
+      this.timeout(5000);
+
+      const originalData = new FormData();
+
+      originalData.append('x', '123');
+
+      server = await startHTTPServer(async (req, res) => {
+
+        const response = await new Response(originalData);
+
+        res.setHeader('Content-Type', response.headers.get('Content-Type'));
+
+        res.end(await response.text());
+      });
+
+      const {data} = await undiciAxios.get('/', {
+        responseType: 'formdata'
+      });
+
+      assert.ok(data instanceof FormData, 'data is not instanceof FormData');
+
+      assert.deepStrictEqual(Object.fromEntries(data.entries()), Object.fromEntries(originalData.entries()));
+    });
+
+    it(`should support json response type`, async () => {
+      const originalData = {x: 'my data'};
+
+      server = await startHTTPServer((req, res) => res.end(JSON.stringify(originalData)));
+
+      const {data} = await undiciAxios.get('/', {
+        responseType: 'json'
+      });
+
+      assert.deepStrictEqual(data, originalData);
+    });
+  });
+
+  describe("progress", () => {
+    describe('upload', function () {
+      it('should support upload progress capturing', async function () {
+        this.timeout(15000);
+
+        server = await startHTTPServer({
+          rate: 100 * 1024
+        });
+
+        let content = '';
+        const count = 10;
+        const chunk = "test";
+        const chunkLength = Buffer.byteLength(chunk);
+        const contentLength = count * chunkLength;
+
+        const readable = stream.Readable.from(async function* () {
+          let i = count;
+
+          while (i-- > 0) {
+            await setTimeoutAsync(1100);
+            content += chunk;
+            yield chunk;
+          }
+        }());
+
+        const samples = [];
+
+        const {data} = await undiciAxios.post('/', readable, {
+          onUploadProgress: ({loaded, total, progress, bytes, upload}) => {
+            console.log(`Upload Progress ${loaded} from ${total} bytes (${(progress * 100).toFixed(1)}%)`);
+
+            samples.push({
+              loaded,
+              total,
+              progress,
+              bytes,
+              upload
+            });
+          },
+          headers: {
+            'Content-Length': contentLength
+          },
+          responseType: 'text'
+        });
+
+        await setTimeoutAsync(500);
+
+        assert.strictEqual(data, content);
+
+        assert.deepStrictEqual(samples, Array.from(function* () {
+          for (let i = 1; i <= 10; i++) {
+            yield ({
+              loaded: chunkLength * i,
+              total: contentLength,
+              progress: (chunkLength * i) / contentLength,
+              bytes: 4,

### Copilot

[nitpick] The use of the magic number '4' for bytes in the progress event is unclear; consider defining a constant or adding a comment to clarify its significance.
```suggestion
              bytes: BYTES_PER_CHUNK,
```

### jasonsaayman

going to ingore this for now

## thread:2101815285

@@ -8,31 +8,31 @@ const knownAdapters = {
   http: httpAdapter,
   xhr: xhrAdapter,
   fetch: fetchAdapter
-}
+};
 
 utils.forEach(knownAdapters, (fn, value) => {
   if (fn) {
     try {
-      Object.defineProperty(fn, 'name', {value});
-    } catch (e) {
-      // eslint-disable-next-line no-empty
+      Object.defineProperty(fn, 'name', { value });
+    } catch (_) {
+      // name property might be read-only; safely ignored

### jasonsaayman

please can you add back the eslint condition under this comment

