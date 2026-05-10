---
title: HTTP Timeout Strategy
description: 'Standardize how you apply timeouts for outbound HTTP requests.


  - If the shared `http.Client` already sets `Timeout`, do **not** also wrap each
  request with `context.WithTimeout` (it’s redundant and can make behavior harder
  to reason about).'
repository: infiniflow/ragflow
label: Networking
language: Go
comments_count: 4
repository_stars: 80174
---

Standardize how you apply timeouts for outbound HTTP requests.

- If the shared `http.Client` already sets `Timeout`, do **not** also wrap each request with `context.WithTimeout` (it’s redundant and can make behavior harder to reason about).
- If the shared `http.Client` does **not** have a safe end-to-end timeout (common for streaming/SSE), avoid `http.Client.Timeout` because it can truncate long-lived bodies. Instead:
  - Apply a request-scoped deadline with `context.WithTimeout` for **non-streaming** calls.
  - For streaming calls, rely on transport-level limits for connection establishment/headers (e.g., `transport.ResponseHeaderTimeout`) and avoid client-level `Timeout`.

Example pattern (non-stream):
```go
// Client: no Timeout when you need long-lived streaming elsewhere
client := &http.Client{Transport: transport} // transport.ResponseHeaderTimeout set

ctx, cancel := context.WithTimeout(context.Background(), nonStreamCallTimeout)
defer cancel()

req, err := http.NewRequestWithContext(ctx, "POST", url, bytes.NewBuffer(jsonData))
resp, err := client.Do(req)
// handle resp
```

Example pattern (client Timeout already set):
```go
// NewModel sets httpClient.Timeout (e.g., 120s) and you don't pass ctx through
req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
resp, err := httpClient.Do(req) // no per-request context timeout wrapper
```

Apply this consistently across drivers so timeout behavior is predictable for both normal responses and SSE/streaming.