---
title: Avoid duplicate HTTP headers
description: Ensure HTTP headers are sent only once per response to prevent network
  protocol violations and connection errors. Sending headers multiple times violates
  HTTP protocol standards and can cause "Broken pipe" errors and connection failures.
repository: ClickHouse/ClickHouse
label: Networking
language: C++
comments_count: 3
repository_stars: 42425
---

Ensure HTTP headers are sent only once per response to prevent network protocol violations and connection errors. Sending headers multiple times violates HTTP protocol standards and can cause "Broken pipe" errors and connection failures.

When working with HTTP responses, be careful not to call methods that send headers (like `response.send()`) before the final response is written. The framework typically handles header transmission automatically during the final write operation.

Example of problematic code:
```cpp
response.setStatusAndReason(Poco::Net::HTTPResponse::HTTP_NO_CONTENT);
response.setChunkedTransferEncoding(false);
response.send(); // ❌ Sends headers prematurely
// ... later in code ...
// Headers sent again automatically - causes protocol violation
```

Example of correct code:
```cpp
response.setStatusAndReason(Poco::Net::HTTPResponse::HTTP_NO_CONTENT);
response.setChunkedTransferEncoding(false);
// ✅ Let the framework send headers during final write operation
```

This applies to all HTTP server implementations and is critical for maintaining stable network connections, especially under high load or in distributed environments where connection reliability is essential.