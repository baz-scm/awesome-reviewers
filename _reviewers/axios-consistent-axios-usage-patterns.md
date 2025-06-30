---
title: "Consistent Axios Usage Patterns"
description: "Maintain consistent usage of the Axios library throughout your Typescript codebase. Pay special attention to consistent error handling, Axios configuration options, Axios request patterns, and Axios response handling."
repository: "axios/axios"
label: "Axios"
language: "TypeScript"
comments_count: 2
repository_stars: 107000
example_comments:
  - comment_author: samavati
    comment_body: |
      Thanks for submitting this fix! Changing isCancel to check for `CanceledError<any>` makes sense. However, I think we can improve the typings further by making `isCancel` generic:

      ```suggestion
      export function isCancel<T = any>(value: any): value is CanceledError<T>;
      ```
    commented_code: |
      @@ -516,7 +517,7 @@ export function isAxiosError<T = any, D = any>(payload: any): payload is AxiosError
       export function spread<T, R>(callback: (...args: T[]) => R): (array: T[]) => R;

-export function isCancel(value: any): value is Cancel;
+export function isCancel(value: any): value is CanceledError<any>;

  - comment_author: Fonger
    comment_body: |
      You should add the equivalent options like brotli does.

      ```js
      const zstdOptions = {
        flush: zlib.constants.ZSTD_e_flush,
        finishFlush: zlib.constants.ZSTD_e_flush
      }
      ```
    commented_code: |
      @@ -524,6 +525,13 @@ export default isHttpAdapterSupported && function httpAdapter(config) {
               streams.push(zlib.createBrotliDecompress(brotliOptions));
               delete res.headers['content-encoding'];
             }
           break;
         case 'zstd':
           if (isZstdSupported) {
             streams.push(zlib.createZstdDecompress());
             delete res.headers['content-encoding'];

  - comment_author: BasixKOR
    comment_body: |
      Sorry for delayed response, I added the relevant part to the commit [e2ba395](https://github.com/axios/axios/pull/6792/commits/e2ba395435f3f7f5260afffc8a3aad2d96159d06).
    commented_code: |
      @@ -524,6 +525,13 @@ export default isHttpAdapterSupported && function httpAdapter(config) {
               streams.push(zlib.createBrotliDecompress(brotliOptions));
               delete res.headers['content-encoding'];
             }
           break;
         case 'zstd':
           if (isZstdSupported) {
             streams.push(zlib.createZstdDecompress());
             delete res.headers['content-encoding'];

  - comment_author: JamieDraperUK
    comment_body: |
      Very minor thing but it might be neater and remove some of the duplication if you stuffed the result the host string building into it's own variable.
      `
      var host = parsed.hostname + parsed.port ? ':' + parsed.port : '';
      `
      Which results in
      `
       options.headers.host = host;
       options = setProxy(options, proxy, protocol + '//' + host + options.path);
      `
    commented_code: |
      @@ -145,17 +172,8 @@ module.exports = function httpAdapter(config) {
         }

         if (proxy) {
-          options.hostname = proxy.host;
-          options.host = proxy.host;
           options.headers.host = parsed.hostname + (parsed.port ? ':' + parsed.port : '');

  - comment_author: chinesedfan
    comment_body: |
      ```suggestion
        // If a proxy is used, any redirects must also pass through the proxy
      ```
    commented_code: |
      @@ -16,6 +16,33 @@ var enhanceError = require('../core/enhanceError');

       var isHttps = /https:?/;

       /**
        *
        * @param {http.ClientRequestArgs} options
---

Maintain consistent usage of the Axios library throughout your Typescript codebase. Pay special attention to the following:

1. **Consistent Error Handling**: Ensure all Axios requests have proper error handling, such as using try/catch blocks to handle network errors, timeouts, and invalid responses. Provide clear and actionable error messages to aid debugging.

2. **Axios Configuration Options**: Leverage Axios configuration options like `timeout`, `headers`, and `baseURL` to ensure consistent behavior across your application. Avoid hardcoding these values in multiple places.

3. **Axios Request Patterns**: Use the appropriate Axios request methods (e.g. `get`, `post`, `put`, `delete`) consistently based on the HTTP verb required by the API. Avoid mixing request types for the same endpoint.

4. **Axios Response Handling**: Extract and handle the response data consistently, whether it's accessing the `data` property or parsing the response body. Ensure error responses are also handled appropriately.

Provide code examples demonstrating best practices for the above Axios usage patterns to help developers write maintainable and robust Axios-based code.