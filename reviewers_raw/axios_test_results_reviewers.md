# Code Reviewers

Generated from: `../../../axios_test_results.json`  
Total reviewers: **18**


## Reviewer 1: Type-safe API interfaces design

**Label:** `api`  
**Language:** `Typescript`  
**Discussion IDs:** 5 discussions  

### Description

Design API interfaces with strong type safety while maintaining excellent developer experience. Prefer explicit types over loose ones to enable better IDE support and catch errors at compile time.

Key principles:
1. Use explicit generic parameters with meaningful names
2. Prefer `unknown` over `any` for better type safety
3. Use intersection types when combining interface properties
4. Avoid string literals when specific types are available

Example:
```typescript
// ❌ Avoid
interface ApiConfig {
  headers?: Record<string, any>;
  data?: any;
}

// ✅ Better
interface ApiConfig<ResponseData = unknown, RequestData = unknown> {
  headers?: HeadersDefaults & RequestHeaders;
  data?: RequestData;
  response?: AxiosResponse<ResponseData>;
}
```

This approach provides better IDE autocompletion, makes the code more maintainable, and catches potential type errors during development rather than at runtime.

### Suggested Modules

- **** → `**/*.ts`

### Discussion References

- `3a5f8548-1293-457e-8c99-9a7b777db0e6`
- `7ee9afce-737b-4df4-84ff-81835ef10144`
- `788f2104-353f-4422-b780-4a243d5af80d`
- `362f739d-c164-4370-9fa3-9bec0bc2a763`
- `bc0d5575-39cf-4aba-b507-90000e2b9641`

---

## Reviewer 2: Consistent semicolon usage

**Label:** `code style`  
**Language:** `Typescript`  
**Discussion IDs:** 2 discussions  

### Description

Always terminate statements with explicit semicolons to maintain consistency with the existing codebase style. Avoid relying on JavaScript's automatic semicolon insertion (ASI) feature, as this can lead to inconsistent code appearance and potential subtle bugs. Project convention shows that 99% of statements already use explicit semicolons.

Example (incorrect):
```javascript
const headers = new AxiosHeaders({foo: "bar"})
```

Example (correct):
```javascript
const headers = new AxiosHeaders({foo: "bar"});
```

### Suggested Modules

- **** → `**/*.ts`

### Discussion References

- `25a927cb-310a-4265-8938-c7699d5865c5`
- `3fd0b1ec-6995-4aba-8f06-ec9ba0e822ef`

---

## Reviewer 3: Flexible configuration design

**Label:** `configurations`  
**Language:** `Typescript`  
**Discussion IDs:** 2 discussions  

### Description

Design configuration interfaces to be flexible and extensible rather than overly specific. When creating configuration objects:

1. Make configuration parameters optional when possible with sensible defaults
2. Allow for arbitrary additional properties rather than creating specific fields for custom configurations

**Example - Instead of this:**
```typescript
export interface AxiosRequestConfig<D = any> {
  // other properties...
  customConfig?: Record<string, any>;
}

// Required configuration parameter
getUri(config: AxiosRequestConfig): string;
```

**Do this:**
```typescript
export interface AxiosRequestConfig<D = any> {
  // other properties...
  [key: string]: any; // Allow arbitrary properties
}

// Optional configuration parameter
getUri(config?: AxiosRequestConfig): string;
```

This approach allows consumers to extend configurations naturally without requiring interface changes for each new use case, while maintaining backward compatibility through sensible defaults.

### Suggested Modules

- **** → `**/*.ts`

### Discussion References

- `66bca0c4-75ad-496b-a564-131cacbe89b7`
- `d30a5aff-4ffb-4a14-bbf1-66e032edc01d`

---

## Reviewer 4: Standardize null value checks

**Label:** `null handling`  
**Language:** `Javascript`  
**Discussion IDs:** 5 discussions  

### Description

Always use consistent patterns and utility functions for handling null and undefined values. This improves code reliability and maintainability while preventing common errors.

Key guidelines:
1. Use utility functions (like isUndefined, isNull) instead of direct comparisons
2. Prefer empty collections over null for container types
3. Use explicit null checks when dealing with potentially undefined objects

Example:
```javascript
// ❌ Avoid direct null/undefined checks
if (typeof value === 'undefined' || value === null) {
  // ...
}

// ✅ Use utility functions
if (utils.isUndefined(value) || utils.isNull(value)) {
  // ...
}

// ❌ Avoid setting null for collections
this.handlers = null;

// ✅ Use empty collections instead
this.handlers = [];

// ❌ Avoid unsafe property access
if (payload && payload.isAxiosError) {
  // ...
}

// ✅ Use comprehensive null checks
if (!!payload && typeof payload === 'object' && payload.isAxiosError) {
  // ...
}
```

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `cf9bd7e2-4a5e-4fae-b0c6-4f26298f89bf`
- `b4ac6410-0141-40ed-a37e-abd1ee8fa74e`
- `6107488e-a86f-42ff-9a3d-cbfe684aaef9`
- `ebf169be-5e2e-4fa6-aa99-7b9c8ca87466`
- `4446c955-12cd-46e5-a328-f81f3794b0a6`

---

## Reviewer 5: Extract for better readability

**Label:** `code style`  
**Language:** `Javascript`  
**Discussion IDs:** 4 discussions  

### Description

Complex expressions and repeated code should be extracted into well-named variables to improve readability and maintainability. This applies to:
- Repeated string/value combinations
- Complex conditional logic
- Array transformations
- URL or path constructions

Example - Instead of:
```javascript
if ([options.path, responseDetails.headers.location].every(item => item === '/foo')) {
  // ...
}
```

Better approach:
```javascript
const isPathMatching = options.path === '/foo';
const isLocationMatching = responseDetails.headers.location === '/foo';
if (isPathMatching && isLocationMatching) {
  // ...
}
```

This practice:
- Makes code self-documenting through meaningful variable names
- Reduces cognitive load when reading complex logic
- Makes debugging easier by providing clear intermediate values
- Prevents duplicate calculations

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `c8d46afb-9021-4971-8187-4bfed4f442c0`
- `35dc47c8-c263-4957-bcf0-403f5cecd069`
- `e36f6fdc-69a7-4fba-8bd4-55714e99224d`
- `b90c4025-cbfc-49dc-bb8a-539ad2077fa2`

---

## Reviewer 6: Proxy protocol handling

**Label:** `networking`  
**Language:** `Javascript`  
**Discussion IDs:** 5 discussions  

### Description

When implementing HTTP clients with proxy support, ensure the connection to the proxy uses the protocol specified in the proxy configuration (not the request protocol). This is crucial for scenarios like accessing HTTPS resources through an HTTP proxy.

Key implementation guidelines:
- Use the proxy's protocol for the connection to the proxy server
- Implement HTTP CONNECT tunneling for HTTPS destinations through proxies
- Parse proxy URLs correctly using the `hostname` property (not `host`)
- Support common proxy environment variables including fallbacks

```javascript
function configureProxy(options, config) {
  // Check for explicitly configured proxy
  let proxy = config.proxy;
  
  if (!proxy) {
    // Check for environment variables
    const proxyEnv = parsed.protocol.slice(0, -1) + '_proxy';
    const proxyUrl = process.env[proxyEnv] || 
                     process.env[proxyEnv.toUpperCase()] ||
                     process.env.all_proxy || 
                     process.env.ALL_PROXY;
    
    if (proxyUrl) {
      const parsedProxyUrl = url.parse(proxyUrl);
      proxy = {
        host: parsedProxyUrl.hostname,  // Use hostname, not host (which includes port)
        port: parsedProxyUrl.port,
        protocol: parsedProxyUrl.protocol
      };
      
      // Handle proxy authentication if present
      if (parsedProxyUrl.auth) {
        // Configure proxy authentication
      }
    }
  }
  
  if (proxy) {
    // Use proxy's protocol for connection to proxy
    // Set up tunneling for HTTPS requests through HTTP proxy
    const usesTunnel = proxy.protocol === "http:" && options.protocol === "https:";
    if (usesTunnel) {
      // Configure HTTP CONNECT tunneling
    }
  }
  
  return options;
}
```

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `b0ead9cc-30f5-41d3-b44d-9c0454f21045`
- `5d257fe3-2e42-4081-86c7-c70f930e1517`
- `7ec063c5-7320-4993-a1c9-920a5c965d29`
- `2b321279-2c52-4ee5-b1b0-04c0fa5db019`
- `b1b00342-c8f9-44c2-b5f2-edc68f0abc86`

---

## Reviewer 7: Consistent method behaviors

**Label:** `api`  
**Language:** `Javascript`  
**Discussion IDs:** 5 discussions  

### Description

Design API methods with predictable behavior patterns that follow common conventions. Methods that modify objects directly (`setSth()`) should not return values unless supporting method chaining. Methods that retrieve or transform data (`getSth()`) should return new objects without modifying inputs. Public class interfaces should maintain backward compatibility even if not all functionality is used internally. Ensure method signatures clearly indicate whether they accept request bodies:

```javascript
// Good - clear behavior from naming and return type
function setHeaders(config, headers) {
  config.headers = headers;
  // No return, modifies object directly
}

function getHeaders(config) {
  // Returns new object, doesn't modify input
  return {...config.headers};
}

// Support method chaining explicitly
function addHeader(config, key, value) {
  config.headers[key] = value;
  return this; // Explicitly returns for chaining
}
```

When adding features to public APIs, ensure all methods have consistent signatures, behavior, and documentation, even if some functionality isn't used in your codebase yet.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `e91324a9-084a-4bec-9685-87e54d156eff`
- `714e68ee-4ab0-4c50-bb3f-98bfb4126918`
- `23d3fcf5-4e12-4799-a8e0-fa8bf993336a`
- `98bb4304-4200-44bb-9bec-9947edebfd97`
- `26201214-2bd0-4116-a372-0114d125a2d0`

---

## Reviewer 8: Validate security-critical inputs

**Label:** `security`  
**Language:** `Javascript`  
**Discussion IDs:** 4 discussions  

### Description

Always validate and sanitize user-supplied inputs before using them in security-sensitive operations. This helps prevent multiple types of vulnerabilities including Server-Side Request Forgery (SSRF), prototype pollution, and command injection.

For URL validation to prevent SSRF attacks:
```javascript
// When handling user input that affects URLs
try {
  const ssrfAxios = axios.create({
    baseURL: 'http://localhost:' + String(GOOD_PORT),
  });
  
  // Validate user input before using in URL paths
  const userId = validateInput(userSuppliedId);
  
  // If validation fails, throw specific error
  if (!isValidUserId(userId)) {
    throw new Error('Invalid URL:' + userId);
  }
  
  const response = await ssrfAxios.get(`/users/${userId}`);
} catch (error) {
  // Handle error appropriately
}
```

For object property validation to prevent prototype pollution:
```javascript
function isPrototypePollutionAttempt(key) {
  // Check for common prototype pollution patterns
  return ['__proto__', 'constructor', 'prototype'].some(
    term => key === term || key.includes('.' + term)
  );
}

// Use when processing user inputs into objects
function safeAddProperty(obj, key, value) {
  if (isPrototypePollutionAttempt(key)) {
    throw new Error('Potential prototype pollution detected');
  }
  obj[key] = value;
}
```

When using user input in command execution contexts, always use parameterized approaches instead of string concatenation to prevent command injection.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `345bee55-45a3-4033-bb30-f9cc8394d253`
- `2cfc2d88-c48b-42f7-8742-7955aca42eaa`
- `aec5b545-f798-4953-b8f9-7ef0f8e5c17e`
- `62e6a236-c21f-43bf-a604-8a819243ed57`

---

## Reviewer 9: Complete error handling chain

**Label:** `error handling`  
**Language:** `Javascript`  
**Discussion IDs:** 5 discussions  

### Description

Implement comprehensive error handling throughout the codebase by ensuring all error scenarios are properly caught, typed, and propagated. This includes:

1. Always include catch blocks for async operations
2. Properly type and propagate error information
3. Use standardized error codes for consistent error handling
4. Ensure error callbacks receive and handle error parameters

Example:
```javascript
// Bad
import(modulePath)
  .then(module => {
    module.default(req, res);
  });

// Good
import(modulePath)
  .then(module => {
    module.default(req, res);
  })
  .catch(error => {
    // Properly typed error with standardized code
    const err = new Error('Module load failed');
    err.code = 'EMODLOAD';
    err.cause = error;
    errorHandler(err);
  });

// For error callbacks
service.use(
  (config) => { /* ... */ },
  (error) => {
    // Properly handle error parameter
    errorLogger(error);
    throw error; // Propagate if needed
  }
);
```

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `4c397903-e925-48ba-a717-7be2bc363187`
- `ed4349ec-d6d7-4aaf-9f06-78974dff4b2b`
- `5b23491d-2361-48c3-ba2d-3c5a2a7ec83a`
- `effb958e-3a37-4f83-99df-e2616dc45d2c`
- `ccdf32d8-486d-4188-85e3-654cd3dabda6`

---

## Reviewer 10: Configuration property standards

**Label:** `configurations`  
**Language:** `Javascript`  
**Discussion IDs:** 3 discussions  

### Description

Always define configuration properties with sensible defaults and consistent naming conventions. When adding new configurable features, establish clear defaults that follow platform conventions and document their purpose.

Guidelines:
- Group related configuration properties together in a structured object
- Use descriptive names that clearly indicate the property's purpose
- Provide sensible defaults that work in most common scenarios
- Document the expected values and behavior of each configuration option

Example:
```javascript
const defaults = {
  // HTTP request defaults
  headers: {
    common: {
      'Accept': 'application/json, text/plain, */*'
    }
  },
  
  // Fetch-related configurations
  fetcher: null,
  fetchOptions: {
    cache: 'default',
    redirect: 'follow'
  },
  
  // Character encoding settings
  charset: 'utf-8',
  
  // Feature flags
  experimental_http2: false
};
```

For experimental features, use clearly named boolean flags (like `experimental_http2`). For encoding or format settings, follow platform conventions and provide fallbacks where appropriate (e.g., `config.charset || 'utf-8'`). This approach ensures configurations are discoverable, maintainable, and properly understood by all developers.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `1d983bf6-2a88-469d-934a-04725d77d19a`
- `cbc793f6-a4ec-40cb-83f1-694baa978c0a`
- `c54ea06b-3b29-4d15-8ffa-8b7872b11e0f`

---

## Reviewer 11: Specific test assertions

**Label:** `testing`  
**Language:** `Javascript`  
**Discussion IDs:** 5 discussions  

### Description

When writing tests, explicitly assert specific conditions and expected values rather than relying on general success/failure checks. This prevents tests from silently passing when they should fail and ensures tests verify exactly what they're intended to verify.

Three key practices to follow:

1. **Handle promise rejections explicitly** - Always include catch clauses in promise chains and pass errors to the done callback:
```javascript
axios.get('http://localhost:4444/')
  .then(function(res) {
    // assertions here
    done();
  }).catch(done); // This ensures test fails if promise rejects
```

2. **Assert specific error conditions** - When testing error cases, verify specific error details rather than just that an error occurred:
```javascript
axios.get('http://localhost:4444/')
  .catch(function(error) {
    assert.equal(error.code, 'ERR_FR_TOO_MANY_REDIRECTS');
    // Test specific error conditions, not just that an error happened
    done();
  });
```

3. **Include explicit expected values** - Use literal expected values in assertions rather than relying on functions with unclear output:
```javascript
// Bad: Hard to see expected value
expect(buildURL('/foo', {date: date})).toEqual('/foo?date=' + date.toISOString());

// Better: Shows exact expected output
expect(buildURL('/foo', {date: date})).toEqual('/foo?date=' + encodeURIComponent(date.toISOString()));
```

Following these practices makes tests more reliable indicators of correct behavior and easier to debug when they fail.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `69dbe255-e096-45bb-a40e-811a795edcd8`
- `40018386-cc6c-415b-931a-cf94d1c2f94e`
- `461d6402-fe15-495a-9aef-4307c0d9b160`
- `104b8e70-141c-4a8d-b27e-a5c061f5d574`
- `70ea283c-bbd0-4788-b1cf-8efa3f200cc2`

---

## Reviewer 12: Documentation reflects reality

**Label:** `documentation`  
**Language:** `Markdown`  
**Discussion IDs:** 5 discussions  

### Description

Always ensure documentation accurately represents the actual code behavior and implementation details. Include important contextual information such as:

1. Platform-specific limitations (e.g., "Node only" features)
2. Explanations for deprecated features with recommended alternatives
3. Precise descriptions of function parameters and behaviors
4. Concise, merged code examples to demonstrate functionality

When documenting APIs, verify that your descriptions match the actual implementation rather than the intended design. For example, if a function behaves differently than originally designed, update the documentation to reflect the actual behavior:

```js
// INCORRECT DOCUMENTATION
// `validateStatus` defines whether to resolve or reject the promise for a given
// HTTP response status code. If `validateStatus` returns `true` (or is set to `null`
// or `undefined`), the promise will be resolved; otherwise, the promise will be rejected.

// CORRECT DOCUMENTATION
// `validateStatus` defines whether to resolve or reject the promise for a given
// HTTP response status code. If `validateStatus` returns `true` (or is set to `null`), 
// the promise will be resolved; otherwise, the promise will be rejected.
```

For deprecated features, clearly indicate:
```
~~Concurrency~~
Deprecated. Use `Promise.all` to replace them.
```

Keep documentation concise by consolidating related code examples when possible.

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `2591f55d-b3a4-4626-a732-8c99509724ce`
- `ce743ca0-e4cc-44f1-9830-9d3acb8ae4de`
- `683f05f7-533f-42a3-9f8d-2ed52b4f804d`
- `e9489145-5574-4ff6-a807-335c8c5946c2`
- `8b7eb061-8563-454a-a3e2-1a3fc31abe04`

---

## Reviewer 13: User-friendly error messages

**Label:** `error handling`  
**Language:** `Html`  
**Discussion IDs:** 2 discussions  

### Description

Error messages should be concise and clearly communicate what went wrong without unnecessary verbosity. When implementing error handling, maintain consistent code style and organize related operations logically within appropriate blocks.

Example:
```javascript
// Instead of this:
try {
    data = JSON.parse(data);
} catch (e) {
    output.innerHTML = "Error : Is blank or not JSON string type. Please check your data.";
    data = null;
}

// Do this:
try {
    data = JSON.parse(data);
    
    // Keep related operations in the try block
    axios.post('/post/server', data)
        .then(function (res) {
            output.className = 'container';
            output.innerHTML = res.data;
        })
        .catch(function (err) {
            output.className = 'container text-danger';
            output.innerHTML = err.message;
        });
} catch (e) {
    // Use concise, clear error messages
    output.innerHTML = "Error: empty string or invalid JSON";
    output.className = 'container text-danger';
}
```

This approach improves user experience by providing clear feedback while maintaining clean, logically structured code with consistent styling.

### Suggested Modules

- **** → `**/*.html`

### Discussion References

- `a499c4f5-054b-4bdd-a9ea-9643c4bb69a7`
- `e84a8a4e-1c82-4924-9998-966597ad0f68`

---

## Reviewer 14: Robust Axios Usage in Typescript

**Label:** `axios`  
**Language:** `Typescript`  
**Discussion IDs:** 4 discussions  

### Description

This review focuses on ensuring robust and type-safe usage of the Axios library in Typescript codebases. Key recommendations:

1. Leverage Axios' built-in type-checking utilities rather than relying on error-prone `instanceof` checks. Use `axios.isCancel()` to detect canceled requests instead of manual type checking.

2. Properly handle Content-Type headers when sending data. Document how Axios automatically manages Content-Type for different data types (e.g. JSON, form data, URL-encoded). Provide clear examples of correct data transformation before sending, such as using `URLSearchParams` for URL-encoded form data.

3. Standardize serialization patterns for complex data types like `FormData` and nested objects to ensure consistent data handling across the codebase.

Following these practices will help ensure your Axios-based APIs remain robust and maintainable when used in applications with varying dependency versions, environments (browser/Node.js), and data formats.

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `a4b27d81-1c23-4a50-9c76-bb443ed3ce5e`
- `5154e458-2f76-4470-8c26-84c84e0ace1f`
- `12498769-9c66-4b40-97df-cfe1627f993e`
- `a9e8b3da-2437-4031-9d43-b0e06f2d41cd`

---

## Reviewer 15: Proper Error Handling in Axios Typescript Code

**Label:** `axios`  
**Language:** `Typescript`  
**Discussion IDs:** 4 discussions  

### Description

As a code reviewer, it is important to ensure that Axios-based Typescript code properly handles and propagates errors. Key recommendations:

1. Use `console.error()` instead of `console.log()` when logging errors to maintain complete error context.
2. When handling Axios promise rejections, always preserve the full error object rather than just the error message. This provides downstream error handlers with the necessary information for debugging.
3. Follow established Axios error handling patterns, such as using `.catch()` blocks in promise chains to centralize error logging and potential recovery logic.
4. Ensure consistent error handling approaches are used throughout the codebase, such as always including the full error object when logging or rejecting promises.

Example of proper Axios error handling in Typescript:

```typescript
// In Axios interceptors, preserve the full error object
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error(error);
    return Promise.reject(error);
  }
);

// In promise chains, use consistent error handling
axios.get('/user?ID=12345')
  .then((response) => {
    // handle success
    console.log(response.data);
  })
  .catch((error) => {
    console.error(error);
    // Consider error recovery or propagation needs
  })
  .finally(() => {
    // always executed
  });
```

This approach enables better debugging, maintains backward compatibility, and follows established Axios error handling conventions.

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `4588b27b-2475-4237-bf4f-375fd85d7f9b`
- `03e3deec-280b-41a4-a10b-42e876f3e136`
- `2112c169-6b7e-435c-acf9-6b22b62c4439`
- `9e7ea08e-06bf-4c81-80fb-69fbd897bc13`

---

## Reviewer 16: Proper Axios Configuration and Usage

**Label:** `axios`  
**Language:** `Typescript`  
**Discussion IDs:** 3 discussions  

### Description

When implementing code that uses the Axios library in TypeScript, it is important to follow best practices for configuring and accessing Axios instances and settings. Ensure that:

1. Axios instances are properly configured with appropriate defaults, such as timeout values and custom properties.
2. Configuration properties are accessed correctly, using the proper namespacing and access paths.
3. Request-specific configuration overrides instance-level defaults in a predictable manner.

For example, when creating an Axios instance:

```typescript
// GOOD: Clearly document Axios instance configuration
// Configuration precedence order:
// 1. Library defaults
// 2. Instance defaults
// 3. Request-specific config (overrides instance defaults for url, method, params, data)

const instance = axios.create({
  timeout: 5000,
  customConfig: { retryOnError: true } // Custom properties in their own namespace
});

// Access custom config properly
if (config && instance.customConfig.retryOnError) {
  // Handle retry logic
}
```

This ensures that developers working on the codebase understand how Axios configuration is resolved, preventing unexpected behavior from improperly merged settings and maintaining clear separation between standard and custom configuration properties.

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `a6fd9e2b-b7e1-451c-a4cc-b7c69ceb2ba7`
- `76a40fdb-7ed7-4710-a081-abf0aa728884`
- `a40599d5-cd71-41ab-88c9-f3cf2186a3ef`

---

## Reviewer 17: Consistent Axios Usage Patterns

**Label:** `axios`  
**Language:** `Typescript`  
**Discussion IDs:** 2 discussions  

### Description

Maintain consistent usage of the Axios library throughout your Typescript codebase. Pay special attention to the following:

1. **Consistent Error Handling**: Ensure all Axios requests have proper error handling, such as using try/catch blocks to handle network errors, timeouts, and invalid responses. Provide clear and actionable error messages to aid debugging.

2. **Axios Configuration Options**: Leverage Axios configuration options like `timeout`, `headers`, and `baseURL` to ensure consistent behavior across your application. Avoid hardcoding these values in multiple places.

3. **Axios Request Patterns**: Use the appropriate Axios request methods (e.g. `get`, `post`, `put`, `delete`) consistently based on the HTTP verb required by the API. Avoid mixing request types for the same endpoint.

4. **Axios Response Handling**: Extract and handle the response data consistently, whether it's accessing the `data` property or parsing the response body. Ensure error responses are also handled appropriately.

Provide code examples demonstrating best practices for the above Axios usage patterns to help developers write maintainable and robust Axios-based code.

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `8195c250-28e9-4292-bc2a-721896706999`
- `d3e0d209-90f4-4c5c-a558-7619372a29ad`

---

## Reviewer 18: Consistent Naming Conventions for Axios Requests and Responses

**Label:** `axios`  
**Language:** `Typescript`  
**Discussion IDs:** 3 discussions  

### Description

When using the Axios library in Typescript, it is important to follow consistent naming conventions to improve code readability and maintainability. Specifically:

1. Use the "on" prefix for Axios event handlers and callbacks, such as `onUploadProgress` and `onDownloadProgress`.
2. Use domain-specific prefixes like "response" to clarify the scope of Axios-related functionality, such as `responseEncoding` and `responseType`.
3. Maintain consistent naming patterns for similar Axios-related functionality, such as using the same parameter structure for authentication-related properties.
4. Align Axios-specific naming with established conventions in the Typescript ecosystem, such as using camelCase for properties and methods.

Following these practices will help developers working on your Axios-based code understand the purpose and usage of your API more intuitively. Provide clear, well-named Axios-related functionality to improve the developer experience.

Example:
```typescript
// ✅ Good - Clear event handler naming with "on" prefix
const config: AxiosRequestConfig = {
  onUploadProgress: (progressEvent: ProgressEvent) => { /* ... */ },
  onDownloadProgress: (progressEvent: ProgressEvent) => { /* ... */ }
}

// ❌ Bad - Unclear purpose of the function
const config: AxiosRequestConfig = {
  uploadProgress: (progressEvent: ProgressEvent) => { /* ... */ },
  downloadProgress: (progressEvent: ProgressEvent) => { /* ... */ }
}

// ✅ Good - Consistent parameter structure and clear scope
const config: AxiosRequestConfig = {
  responseEncoding: 'utf-8',
  proxy: {
    auth: { username: 'mikeymike', password: 'rapunz3l' } // Matches other auth patterns
  }
}
```

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `cd321c3e-27d7-47fe-89c9-8362cbd58551`
- `cbaf3a9f-49d4-4419-b7c2-8bb80f816b85`
- `6f484fd9-baa6-40a6-acee-e828768074e2`

---
