---
title: Test security boundaries
description: Security mechanisms should be tested for both success and failure scenarios
  to ensure they properly enforce boundaries. Don't just test that security features
  work when enabled - also verify they correctly block unauthorized access when disabled
  or misconfigured.
repository: cloudflare/agents
label: Security
language: TypeScript
comments_count: 2
repository_stars: 2312
---

Security mechanisms should be tested for both success and failure scenarios to ensure they properly enforce boundaries. Don't just test that security features work when enabled - also verify they correctly block unauthorized access when disabled or misconfigured.

For CORS implementations, test that cross-origin requests fail without proper headers:

```typescript
it("should reject cross-origin requests without CORS headers", async () => {
  const request = new Request("http://localhost/agents/TestAgent/test", {
    method: "POST",
    headers: {
      Origin: "https://malicious-site.com"
    }
  });

  const response = await routeAgentRequest(request, env, { cors: false });
  
  expect(response.status).toBe(403); // or appropriate error status
  expect(response.headers.get("Access-Control-Allow-Origin")).toBeNull();
});
```

For authentication flows, create comprehensive test suites that cover edge cases, error conditions, and security boundaries rather than just happy path scenarios. Complex security mechanisms like OAuth require dedicated test coverage to ensure all attack vectors are properly defended against.