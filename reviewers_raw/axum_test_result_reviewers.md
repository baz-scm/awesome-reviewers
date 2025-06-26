# Code Reviewers

Generated from: `../../../axum_test_result.json`  
Total reviewers: **16**


## Reviewer 1: Type-safe flexible APIs

**Label:** `api`  
**Language:** `Rust`  
**Discussion IDs:** 10 discussions  

### Description

Design APIs that favor both type safety and flexibility. Use strongly typed wrappers instead of primitive types, but accept generic parameters where flexibility is beneficial.

For headers and content types, use typed wrappers rather than strings:

```rust
// Instead of:
fn get_page(app: Router, path: &str) -> (StatusCode, String, String) // String for content-type
    
// Prefer:
fn get_page(app: Router, path: &str) -> (StatusCode, headers::ContentType, Vec<u8>)
```

Accept more general trait bounds instead of specific types for parameters:

```rust
// Instead of:
pub async fn from_path(path: PathBuf) -> io::Result<FileStream<AsyncReaderStream>>

// Prefer:
pub async fn from_path(path: impl AsRef<Path>) -> io::Result<FileStream<AsyncReaderStream>>
```

Use more general parameter types when possible:

```rust
// Instead of:
pub fn from_bytes(bytes: &Bytes) -> Result<Self, JsonRejection>

// Prefer:
pub fn from_bytes(bytes: &[u8]) -> Result<Self, JsonRejection>
```

Leverage existing conversion mechanisms rather than duplicating types, allowing users to map between your API and domain types:

```rust
// Instead of copying a CloseCode enum, expose a u16 and let users convert
socket.send(Message::Close(Some(CloseFrame {
    code: axum::extract::ws::close_code::NORMAL, // Use constants instead of magic numbers
    // ...
})))
```

Provide ergonomic builder methods, but also implement standard traits like `FromIterator` to support more idiomatic usage patterns:

```rust
// Support both explicit additions and collection-based construction
let form1 = MultipartForm::new().add_part(part1).add_part(part2);
let form2 = MultipartForm::from_iter([part1, part2]);
```

For constructors, follow consistent patterns across related types, making both empty initialization and conversion from domain objects simple:

```rust
// Empty jar: CookieJar::new(), SignedCookieJar::new(key)
// With headers: CookieJar::from_headers(headers), SignedCookieJar::from_headers(headers, key)
```

When documenting your API, explicitly mention behaviors like content-type handling to avoid surprises:
"The Protocol Buffer extractor does not check the `content-type` header."

### Suggested Modules

- **** → `**/*.rs`

### Discussion References

- `9819733d-1fc1-4c14-b6b3-2d62d1d9e54d`
- `90541604-bd06-455b-9a11-f7762f1ed82e`
- `8056636a-9138-4d89-8b91-461bb3584c99`
- `1cdccba6-d316-47eb-9cbb-02f233886ef7`
- `1d9ae46e-031f-4682-94ab-4f26f5836dd4`
- ... and 5 more

---

## Reviewer 2: Prefer descriptive over brief

**Label:** `naming conventions`  
**Language:** `Rust`  
**Discussion IDs:** 5 discussions  

### Description

Choose clear, descriptive names over abbreviated or shortened versions. Names should be self-documenting and follow Rust conventions. While brevity can be tempting, the clarity and maintainability benefits of descriptive names outweigh the extra characters.

Good practices:
- Use full, meaningful names instead of abbreviations
- Follow Rust naming conventions (snake_case for variables/functions, PascalCase for types)
- Use semantic names that describe the purpose
- If external conventions conflict with Rust's, use attributes to maintain both

Example:
```rust
// Instead of:
use axum::http::StatusCode as SC;
const HTML: &str = "text/html";
struct User { _id: u32 }

// Prefer:
use axum::http::StatusCode;
const CONTENT_TYPE_HTML: &str = "text/html";
struct User {
    #[serde(rename = "_id")]  // maintains MongoDB convention while using Rust style
    id: u32
}
```

### Suggested Modules

- **** → `**/*.rs`

### Discussion References

- `292fae37-2172-470b-b979-ac8e44dbcd69`
- `3c49f68a-a31b-4729-b97b-055a72d79ce0`
- `70fa535f-39a7-4ab4-800a-5c3ee93c6d4e`
- `601bce9e-49fc-4982-a1ae-c3a1f227e078`
- `e6458bb0-c4cf-4231-9740-864187422168`

---

## Reviewer 3: Comprehensive documentation standards

**Label:** `documentation`  
**Language:** `Rust`  
**Discussion IDs:** 16 discussions  

### Description

Create clear, well-structured API documentation following these practices:

1. **Use proper formatting**:
   - Separate distinct thoughts with blank lines
   - Ensure consistent paragraph structure
   - Add proper spacing after section headers

```rust
/// Create a multipart form to be used in API responses.
///
/// This struct implements [`IntoResponse`], and so it can be returned from a handler.
```

2. **Use correct references**:
   - Place code elements in backticks with proper linking: [`Type`] not `Type` or Type
   - Use intra-doc links for internal references: `[order-of-extractors]: crate::extract#the-order-of-extractors`
   - Specify version requirements when applicable: "This macro is only available with Rust >= 1.80"

3. **Write informative examples**:
   - Implement documentation tests where possible: `#[doc(test)]`
   - Include complete, runnable code examples
   - Add explanatory comments for complex operations
   - Format examples consistently with proper spacing

4. **Ensure completeness**:
   - Document security implications of sensitive operations
   - Clarify parameter constraints and return value behaviors
   - Use precise language: "This allows sharing state with `IntoResponse` implementations" not "This allows sharing state with IntoResponse implementations"
   - Add trailing periods to documentation sentences

Documentation should be treated as a first-class feature - it's often the first interaction users have with your API.

### Suggested Modules

- **** → `**/*.rs`

### Discussion References

- `cbd1bb62-5be5-4541-bf3e-f71ae3a4e93c`
- `7929f11f-51ec-4e5d-91fc-0cfd53e5f6ca`
- `57fc3520-8cf3-416e-bfef-32fcd55df9dc`
- `7d89003a-c060-4e0e-bcac-b74a8ff5ecf7`
- `60114bdb-f7f4-4d75-9b2b-43ab493d9676`
- ... and 11 more

---

## Reviewer 4: Prefer simpler code constructs

**Label:** `code style`  
**Language:** `Rust`  
**Discussion IDs:** 6 discussions  

### Description

Always opt for simpler, more idiomatic code constructs over complex or verbose alternatives. This includes:

1. Using built-in Rust patterns instead of manual implementations:
```rust
// Instead of
.for_each(|(name, value)| {
    // ... implementation
});

// Prefer
for (name, value) in items {
    // ... implementation
}
```

2. Leveraging pattern matching for cleaner control flow:
```rust
// Instead of
let content_length = req.method().clone();
if content_length > N { ... }

// Prefer
match (content_length, req.method()) {
    (content_length, &(Method::GET | Method::HEAD)) => { ... }
}
```

3. Using method chaining when it improves readability:
```rust
// Instead of
cmd.arg("--body");
cmd.arg(body);

// Prefer
cmd.args(&["--body", body])
```

4. Maintaining consistent formatting:
- Group related imports together
- Avoid mixing inline and non-inline arguments
- Use consistent line wrapping in documentation

The goal is to write code that is easier to read, maintain, and reason about by leveraging Rust's built-in constructs and following consistent patterns.

### Suggested Modules

- **** → `**/*.rs`

### Discussion References

- `5b281204-405f-4c71-8caf-8d139030cefd`
- `414aab5a-7f9a-422c-93d4-bd566d151d8d`
- `6e29f584-4f02-4b71-bd6f-8ec8087b0127`
- `ad75d045-d556-41c3-b1ed-b4ee2b303f35`
- `d8bc2aa3-f78a-44e0-b206-77f9f8e36937`
- ... and 1 more

---

## Reviewer 5: Structure errors for safety

**Label:** `error handling`  
**Language:** `Rust`  
**Discussion IDs:** 4 discussions  

### Description

Create specific error types with appropriate status codes while ensuring sensitive details are logged but not exposed to clients. Follow these guidelines:

1. Define specific error types instead of using generic ones
2. Implement proper status codes for each error variant
3. Log detailed errors internally
4. Return sanitized error messages to clients

Example:
```rust
#[derive(Debug, Error)]
pub enum ApiError {
    #[error("Invalid input provided")]
    ValidationError(#[from] JsonRejection),
    #[error("Internal server error")]
    InternalError(#[source] anyhow::Error),
}

impl IntoResponse for ApiError {
    fn into_response(self) -> Response {
        let status = match &self {
            Self::ValidationError(_) => StatusCode::UNPROCESSABLE_ENTITY,
            Self::InternalError(_) => StatusCode::INTERNAL_SERVER_ERROR,
        };
        
        // Log detailed error internally
        tracing::error!("{:#}", self);
        
        // Return sanitized response to client
        let body = Json(json!({
            "error": self.to_string()  // Uses the #[error] messages
        }));
        
        (status, body).into_response()
    }
}

### Suggested Modules

- **** → `**/*.rs`

### Discussion References

- `7cea6939-eb01-4fa5-8bfd-28267dbf58c2`
- `9eb426c3-1c3b-4691-a953-32d4bcc26efa`
- `685a8b1d-b8ec-4558-aaf3-2581de22c816`
- `f8589031-50e0-4aa4-8392-32c52ba819f9`

---

## Reviewer 6: Handle protocol headers properly

**Label:** `networking`  
**Language:** `Rust`  
**Discussion IDs:** 4 discussions  

### Description

When implementing network services, especially proxies and protocol handlers, proper HTTP header management is critical for correct functionality, compatibility, and diagnostics.

For proxy services:
- Remove or replace the `HOST` header when forwarding requests to avoid conflicts
- Include standard forwarded headers to maintain origin information:
  ```rust
  // Add standard proxy headers
  req.headers_mut().insert(
      "X-Forwarded-Host", 
      original_host.clone()
  );
  req.headers_mut().insert(
      "X-Forwarded-Proto",
      HeaderValue::from_static(original_scheme)
  );
  req.headers_mut().insert(
      "X-Forwarded-For",
      client_ip.to_string().parse().unwrap()
  );
  ```

For protocol upgrades (like WebSockets):
- Validate required headers with specific error messages
  ```rust
  let sec_websocket_key = req
      .headers_mut()
      .remove(header::SEC_WEBSOCKET_KEY)
      .ok_or(WebSocketKeyHeaderMissing)?;
  ```
- Be aware of protocol version differences (HTTP/1.0 doesn't support upgrades, HTTP/1.1 uses GET for WebSockets, later versions use CONNECT)
- Document the last points where protocol-specific data is available:
  ```rust
  /// This is the last point where we can extract TCP/IP metadata such as 
  /// IP address of the client as well as things from HTTP headers
  ```

Proper header handling improves interoperability, makes debugging easier, and creates more robust network applications.

### Suggested Modules

- **** → `**/*.rs`

### Discussion References

- `f4c68830-b55d-437b-86b9-2247e2f50594`
- `7beab17c-cc3a-4745-94ed-a641592d2680`
- `681b6a03-ce44-42c4-85f3-1bb15d61ad05`
- `b3e27fdc-baf0-4b10-b97c-d6d1ea4d0b5b`

---

## Reviewer 7: Lock carefully in async

**Label:** `concurrency`  
**Language:** `Rust`  
**Discussion IDs:** 4 discussions  

### Description

When using locks in async code, follow these critical guidelines:

1. Never hold `std::sync::Mutex` locks across `.await` points as this can cause deadlocks even in single-threaded runtimes. Use `tokio::sync::Mutex` when the lock needs to be held across await points.

2. Consider lock granularity carefully - avoid overly fine-grained locking that could increase complexity and potential deadlocks.

Example of proper mutex usage in async context:

```rust
#[derive(Clone)]
struct AppState {
    // Coarse-grained locking - entire data structure under one lock
    data: Arc<tokio::sync::Mutex<ComplexData>>,
    
    // Fine-grained locking - only when specifically needed
    // Note: Choose granularity based on your specific use case
    counters: Arc<std::sync::Mutex<Counters>>,
}

async fn handle_request(state: AppState) {
    // OK: std::sync::Mutex for quick operations without .await
    let count = state.counters.lock().unwrap().get_count();
    
    // OK: tokio::sync::Mutex for operations involving .await
    let mut data = state.data.lock().await;
    data.update_with_async_operation().await;
} // locks are automatically released at end of scope
```

Remember: The choice between `std::sync::Mutex` and `tokio::sync::Mutex` isn't about thread safety, but about async compatibility. `std::sync::Mutex` is thread-safe but can deadlock if held across `.await` points.

### Suggested Modules

- **** → `**/*.rs`

### Discussion References

- `b98e52f9-7d86-4783-b5d1-d9d8e55a250f`
- `e97c8768-0c5a-4b71-81ac-9c78ebba004a`
- `cdceb89a-bdf9-4ae9-8beb-223228d550c4`
- `f4da1749-77af-4489-b592-81b2968079bc`

---

## Reviewer 8: Minimize memory allocation overhead

**Label:** `performance optimization`  
**Language:** `Rust`  
**Discussion IDs:** 4 discussions  

### Description

Optimize performance by minimizing unnecessary memory allocations and using allocation-efficient APIs. Key practices:

1. Use static data when possible instead of dynamic allocations
2. Leverage specialized types and methods that minimize copies
3. Consider allocation patterns in data transformations

Example - Before:
```rust
// Unnecessary allocation
.send(Message::Ping("Hello, Server!".into()))

// Multiple potential allocations
let string = std::str::from_utf8(&bytes)
    .map_err(InvalidUtf8::from_err)?
    .to_owned();
```

Example - After:
```rust
// Using static data
.send(Message::Ping(Payload::Shared(
    "Hello, Server!".as_bytes().into()
)))

// Direct conversion avoiding copies
let string = String::from_utf8(bytes.into())
    .map_err(InvalidUtf8::from_err)?;
```

For serialization/encoding operations, prefer methods that write directly to pre-allocated buffers rather than creating intermediate allocations. Consider using specialized types like BytesMut when working with byte buffers.

### Suggested Modules

- **** → `**/*.rs`

### Discussion References

- `34d9b52e-34b2-4219-86fb-bc5c6a45b169`
- `bcc633e1-7fc2-47ac-a6ae-3f6d6aad3a76`
- `cff54da7-a882-4fbf-b659-2a23403bd70a`
- `4015a87a-0049-4ceb-93e8-f32879c7be94`

---

## Reviewer 9: Use Option combinators

**Label:** `null handling`  
**Language:** `Rust`  
**Discussion IDs:** 4 discussions  

### Description

Instead of verbose conditional logic, prefer Rust's Option combinators like `map`, `and_then`, and `filter` for handling potentially null values. This creates more concise, readable code that expresses intent clearly and reduces the chance of null-related bugs.

For example, replace:
```rust
let result = if let Some(value) = optional_value {
    Some(process(value))
} else {
    None
};
```

With:
```rust
let result = optional_value.map(process);
```

Similarly, when handling multiple optional values, use `and_then` instead of nested if-lets:
```rust
// Instead of this
let session_cookie =
    if let Ok(TypedHeader(cookie)) = TypedHeader::<Cookie>::from_request(req).await {
        cookie.get(AXUM_SESSION_COOKIE_NAME).map(|x| x.to_owned())
    } else {
        None
    };

// Prefer this
let session_cookie = Option::<TypedHeader<Cookie>>::from_request(req).await
    .and_then(|cookie| Some(cookie.get(AXUM_SESSION_COOKIE_NAME)?.to_owned()));
```

When validating values that might fail, explicitly set to None on failure:
```rust
self.filename = if let Ok(filename) = value.try_into() {
    Some(filename)
} else {
    trace!("Attachment filename contains invalid characters");
    None
};
```

Using Option combinators not only makes code more concise but also makes the intent clearer and reduces the chance of null-handling mistakes.

### Suggested Modules

- **** → `**/*.rs`

### Discussion References

- `8aa2fc88-a067-4512-883e-2788a68fd86f`
- `6ede4943-06c2-4d18-866d-18fc64b898e3`
- `1543e7c0-e969-4ba3-a74f-2bea6b163db7`
- `954f3943-3653-440c-b98e-f3e0f32aae1d`

---

## Reviewer 10: Secure cookie configuration

**Label:** `security`  
**Language:** `Rust`  
**Discussion IDs:** 1 discussions  

### Description

Always set appropriate security flags on cookies, especially those used for authentication or session management. At minimum, include:

1. `HttpOnly` - Prevents JavaScript access to the cookie, protecting against XSS attacks
2. `Secure` - Ensures the cookie is only sent over HTTPS connections
3. `SameSite` - Use `Lax` for cookies needed after redirects (like OAuth flows), or `Strict` for maximum protection when redirects aren't needed

Example of properly configured cookie in an OAuth flow:

```rust
// Attach the session cookie to the response header with security flags
let cookie = format!(
    "{COOKIE_NAME}={cookie}; SameSite=Lax; Path=/; HttpOnly; Secure"
);
```

These settings significantly reduce the risk of cookie theft, session hijacking, and cross-site request forgery attacks.

### Suggested Modules

- **** → `**/*.rs`

### Discussion References

- `9ad8a94e-5dfa-4438-8297-3dd701954a7f`

---

## Reviewer 11: Documentation consistency standards

**Label:** `documentation`  
**Language:** `Markdown`  
**Discussion IDs:** 5 discussions  

### Description

Maintain consistent documentation formatting standards across all project files, especially in changelogs, code examples, and technical documentation. This ensures readability and prevents confusion when documentation is viewed in different contexts.

Key practices to follow:
1. Use consistent formatting for PR references in changelogs - always use parentheses for PR references `([#123])` and include reference links at the bottom of the file
2. Format code elements with backticks in markdown text (e.g., `IntoResponse`, `FromRequest`)
3. Format code examples to clearly demonstrate the intended API usage:
```rust
// GOOD: Clear method chaining that shows which method calls apply to which objects
let app = Router::new().route(
    "/foo",
    get(|| async {})
        .route_layer(ValidateRequestHeaderLayer::bearer("password"))
);

// BAD: Confusing formatting that obscures the method call hierarchy
let app = Router::new()
    .route("/foo", get(|| async {})
    .route_layer(ValidateRequestHeaderLayer::bearer("password"))
);
```
4. Use proper Markdown link syntax consistently - either inline links `[text](url)` or reference-style links `[text][reference]` with the reference defined elsewhere, but not mixed approaches
5. Remember that documentation may be viewed outside GitHub (in editors, package documentation sites), where automatic linking doesn't work

Consistent documentation makes the codebase more approachable and reduces confusion for both contributors and users.

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `9bb0550e-24b3-4299-b769-392b10125757`
- `f945c8f5-c490-444d-aa69-7c2af1953628`
- `9be82251-7de7-401c-8af7-5008cc74f8e3`
- `d8383989-3e74-40e8-ae30-ea1abe3f0a82`
- `32e47af4-39ab-4913-bc7e-26504688308b`

---

## Reviewer 12: Document feature flags

**Label:** `configurations`  
**Language:** `Toml`  
**Discussion IDs:** 3 discussions  

### Description

When configuring feature flags in Cargo.toml, ensure they are properly structured and documented:

1. **Chain feature dependencies correctly** - Features that depend on other features should explicitly list those dependencies:
```toml
# Incorrect:
cookie-signed = ["cookie-lib/signed"]

# Correct:
cookie-signed = ["cookie", "cookie-lib/signed"]
```

2. **Document non-obvious configuration choices** with comments to help other developers understand your reasoning:
```toml
# `default-features = false` to not depend on tokio which doesn't support compiling to wasm
axum = { path = "../../axum", default-features = false }
```

3. **Use appropriate syntax for conditional feature activation**, understanding special operators like `?` for optional dependencies:
```toml
async-read-body = ["dep:tokio-util", "tokio-util?/io"]
```

These practices ensure that your configuration is both functionally correct and easier for other developers to understand and maintain.

### Suggested Modules

- **** → `**/*.toml`

### Discussion References

- `13c96d03-992c-4941-927f-193bebd2733a`
- `b0f50b3c-de67-494a-a0b5-81a6cc0dfd16`
- `de9e31fa-b290-4dc7-a5f3-2a67adece729`

---

## Reviewer 13: Axum Code Review: Interaction Patterns

**Label:** `axum`  
**Language:** `Typescript`  
**Discussion IDs:** 9 discussions  

### Description

When implementing Axum-based applications, it is crucial to ensure that the interaction patterns between components are well-designed and clearly documented. This includes understanding edge cases, limitations, and best practices around state sharing, router nesting, and extractor ordering.

For nested routers, be sure to explicitly document how fallbacks work between the nested components. Provide clear examples showing the order in which fallbacks are handled for different paths.

When using extractors, clearly specify the ordering constraints and provide complete, working examples to demonstrate the correct usage. Extractors that consume the request body must be ordered last.

Carefully consider state sharing mechanisms between routers. Explain how states are merged or propagated, and explicitly note any limitations. This will help other developers avoid common pitfalls when integrating your Axum-based components.

By providing this level of detail and guidance, you can help ensure that developers working with your Axum-based code can understand critical interactions and implement them correctly, avoiding common issues and improving the overall quality and maintainability of the application.

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `8cf40dc9-b391-418d-9e8b-b17a88a2726b`
- `3e14bcd4-752d-45a7-9b86-892b93f17473`
- `cd905c2b-e007-418b-9e5d-56660195fe89`
- `7bed5c02-43b1-4d0c-ae91-5adfc1c87d5b`
- `4e60dde4-25d5-4318-b1dc-36faaa31662d`
- ... and 4 more

---

## Reviewer 14: Consistent axum Usage in Typescript

**Label:** `axum`  
**Language:** `Typescript`  
**Discussion IDs:** 5 discussions  

### Description

When implementing Typescript code that uses the axum package, maintain consistent and idiomatic usage:

1. Always use the lowercase "axum" when referring to the framework, not "Axum".
2. Leverage axum's built-in types and utilities correctly, such as `Router`, `Middleware`, and `RequestBody`.
3. Follow best practices for handling state and dependencies in axum applications, such as using `task_local` to pass state between middleware and handlers.
4. Ensure error handling is properly implemented, with clear and informative error messages returned to clients.
5. Use axum's routing and middleware features effectively to structure your application, avoiding overly complex or nested routing.

Example of correct axum usage in Typescript:

```typescript
import { Router, RequestBody } from '@awslabs/aws-lambda-typescript-runtime';

const router = new Router();

router.get('/', (req) => {
  return { message: 'Hello, axum!' };
});

router.post('/users', async (req: RequestBody<{ name: string }>) => {
  const { name } = req.body;
  // Handle user creation logic here
  return { id: 1, name };
});

export default router;

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `624f411a-508b-4c81-9bfc-1bb2fa0916d3`
- `2f137539-115a-4b64-9485-65360d3767bf`
- `441b94c0-3f8b-4388-a392-f42a7d736347`
- `4537e9df-785a-4f92-8d42-fddf4da8e3e9`
- `f48678af-4e33-4033-8fd9-c574c0cb2ddb`

---

## Reviewer 15: Use Appropriate Concurrency Patterns with Axum

**Label:** `axum`  
**Language:** `Typescript`  
**Discussion IDs:** 2 discussions  

### Description

When building asynchronous Axum applications that share mutable state, it's important to select the right concurrency mechanisms:

1. For general shared state:
   - Use Axum's built-in `Mutex` or `RwLock` to protect access to in-memory data structures
   - Only use asynchronous `Mutex` or `RwLock` when the lock must be held across `.await` points

2. For shared I/O resources (like database connections):
   - Avoid wrapping individual connections in Axum's `Mutex` or `RwLock`, which can lead to deadlocks
   - Prefer using Axum's built-in connection pool (`PoolOptions`) to handle concurrency internally
   - Consider the actor pattern (e.g. using Axum's `Service` and `State`) for complex shared I/O operations

Example:
```typescript
// GOOD: Using Axum's Mutex to protect in-memory state
const counter = new Mutex<number>(0);

// GOOD: Using Axum's connection pool to handle concurrency
const db = await createPool({
  connectionString: 'postgres://...',
  maxConnections: 10,
});

// AVOID: Wrapping I/O resource in Axum's Mutex
// const db = new Mutex(await createConnection('postgres://...'));
```

Choosing the right concurrency pattern in Axum prevents deadlocks, improves performance, and makes your code more maintainable. Always consider what happens when your Axum handler yields while holding a lock.

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `d564074f-944f-46c7-be7e-37de3b157e8e`
- `1cbafe83-5b1d-46c5-85d4-254389762022`

---

## Reviewer 16: Implement Distributed Tracing in Axum Applications

**Label:** `axum`  
**Language:** `Typescript`  
**Discussion IDs:** 2 discussions  

### Description

As an Axum code reviewer, I recommend implementing proper distributed tracing in your Axum-based web applications to ensure observability across service boundaries. Use Axum's built-in middleware layers to consistently instrument your code:

1. **Propagate Request IDs**: Use the `tower_http::request_id` middleware to generate and propagate unique request IDs across service calls. This allows you to correlate requests and trace their flow through your distributed system.

```typescript
import { Router } from '@awslabs/aws-lambda-typescript-runtime';
import { RequestIdLayer } from '@awslabs/aws-lambda-typescript-runtime/middleware';

const app = Router.create()
  .use(RequestIdLayer.create({
    headerName: 'x-request-id',
    generateRequestId: () => crypto.randomUUID()
  }));
```

2. **Implement Structured Logging with Trace Context**: Leverage the `tower_http::trace` middleware to add detailed tracing information to your application logs. This allows you to correlate log entries with specific requests and understand the flow of execution.

```typescript
import { Router } from '@awslabs/aws-lambda-typescript-runtime';
import { TraceLayer } from '@awslabs/aws-lambda-typescript-runtime/middleware';

const app = Router.create()
  .use(TraceLayer.create({
    makeSpan: (req) => {
      return tracing.info('request', {
        requestId: req.headers.get('x-request-id') || 'unknown',
        method: req.method,
        uri: req.url.pathname
      });
    }
  }));
```

3. **Integrate with OpenTelemetry**: Consider using the `@opentelemetry/api` and `@opentelemetry/sdk-node` packages to connect your Axum application to a standardized observability backend, such as Jaeger, Zipkin, or a cloud-native monitoring platform. This allows you to export traces and metrics for deeper analysis and debugging.

By implementing these patterns, you can effectively debug production issues, understand service dependencies, and measure performance across your distributed Axum-based system.

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `2237aff3-27b7-46f9-866e-cbac6b4d6f79`
- `4ce0aab1-dcfe-41b8-8f3b-d8213206607f`

---
